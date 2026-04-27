import argparse
import base64
import copy
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from jsonschema import Draft202012Validator
from openai import BadRequestError, OpenAI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate canonical math semantic JSON from a PNG via OpenAI API."
    )
    parser.add_argument("--image", required=True, help="Path to input PNG image")
    parser.add_argument("--problem-id", required=True, help="problem_id to inject")
    parser.add_argument(
        "--schema-file",
        default="schema/semantic/semantic.v1.json",
        help="Path to canonical semantic schema",
    )
    parser.add_argument(
        "--out-dir",
        default="modu_math/json_from_png/contract_math",
        help="Output directory for generated canonical semantic JSON",
    )
    parser.add_argument(
        "--output-prefix",
        default=None,
        help="Output filename prefix. Defaults to --problem-id",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (default: OPENAI_MODEL env or gpt-5.4-mini)",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def to_openai_strict_schema(schema: dict) -> dict:
    out = copy.deepcopy(schema)

    def walk(node: object) -> None:
        if isinstance(node, dict):
            node_type = node.get("type")
            is_object_type = node_type == "object" or (
                isinstance(node_type, list) and "object" in node_type
            )
            props = node.get("properties")
            if isinstance(props, dict):
                # Keep optional fields optional. Do not force all properties as required.
                required = node.get("required")
                if isinstance(required, list):
                    node["required"] = [k for k in required if k in props]
                else:
                    node["required"] = []
                node["additionalProperties"] = False
                for child in props.values():
                    walk(child)
            elif is_object_type:
                node.setdefault("properties", {})
                required = node.get("required")
                if isinstance(required, list):
                    node["required"] = required
                else:
                    node["required"] = []
                node["additionalProperties"] = False

            items = node.get("items")
            if items is not None:
                walk(items)
            for key in ("anyOf", "allOf", "oneOf"):
                value = node.get(key)
                if isinstance(value, list):
                    for child in value:
                        walk(child)
            for key in ("$defs", "definitions"):
                value = node.get(key)
                if isinstance(value, dict):
                    for child in value.values():
                        walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(out)
    return out


def image_to_data_url(image_path: Path) -> str:
    b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def ensure_confidence_fields(payload: dict, default_confidence: float = 0.5) -> None:
    domain = payload.get("domain")
    if isinstance(domain, dict):
        objects = domain.get("objects")
        if isinstance(objects, list):
            for item in objects:
                if isinstance(item, dict) and "confidence" not in item:
                    item["confidence"] = default_confidence

        relations = domain.get("relations")
        if isinstance(relations, list):
            for item in relations:
                if isinstance(item, dict) and "confidence" not in item:
                    item["confidence"] = default_confidence

    answer = payload.get("answer")
    if isinstance(answer, dict) and "confidence" not in answer:
        answer["confidence"] = default_confidence

    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and "extraction_confidence" not in metadata:
        metadata["extraction_confidence"] = default_confidence


def generate_semantic(
    client: OpenAI,
    model: str,
    schema: dict,
    data_url: str,
    problem_id: str,
    image_path: Path,
) -> dict:
    base_input = [
        {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "You generate strict canonical JSON for Korean math worksheet parsing. "
                        "Return only a JSON object that satisfies the given schema."
                    ),
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": (
                        "Create canonical semantic JSON from this PNG. "
                        f"Set `problem_id` to `{problem_id}` exactly. "
                        "Include confidence fields for domain.objects, domain.relations, and answer. "
                        "Use conservative confidence values when uncertain."
                    ),
                },
                {"type": "input_image", "image_url": data_url, "detail": "high"},
            ],
        },
    ]

    try:
        response = client.responses.create(
            model=model,
            input=base_input,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "modu_math_semantic_v1",
                    "strict": True,
                    "schema": to_openai_strict_schema(schema),
                }
            },
        )
        payload = json.loads(response.output_text)
    except BadRequestError as exc:
        if "invalid_json_schema" not in str(exc):
            raise
        fallback_input = base_input + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Follow this JSON schema exactly. Output JSON only.\n"
                            + json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
                        ),
                    }
                ],
            }
        ]
        response = client.responses.create(
            model=model,
            input=fallback_input,
            text={"format": {"type": "json_object"}},
        )
        payload = json.loads(response.output_text)

    payload["problem_id"] = problem_id
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        payload["metadata"] = metadata
    metadata.setdefault("source_type", "png")
    metadata.setdefault("source_path", str(image_path))
    ensure_confidence_fields(payload, default_confidence=0.5)

    Draft202012Validator(schema).validate(payload)
    return payload


def main() -> None:
    load_dotenv()
    args = parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your environment or .env file."
        )

    image_path = Path(args.image).resolve()
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if image_path.suffix.lower() != ".png":
        raise ValueError("Only PNG is supported in this script. Use a .png file.")

    schema_path = Path(args.schema_file).resolve()
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    schema = load_json(schema_path)

    model = args.model or os.getenv("OPENAI_MODEL") or "gpt-5.4-mini"
    client = OpenAI()
    data_url = image_to_data_url(image_path)

    semantic = generate_semantic(
        client=client,
        model=model,
        schema=schema,
        data_url=data_url,
        problem_id=args.problem_id,
        image_path=image_path,
    )

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = args.output_prefix or args.problem_id
    out_path = out_dir / f"{prefix}.semantic.contract.v1.json"
    out_path.write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Generated canonical semantic JSON: {out_path}")


if __name__ == "__main__":
    main()
