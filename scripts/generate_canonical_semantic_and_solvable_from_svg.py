import argparse
import copy
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from jsonschema import Draft202012Validator
from openai import BadRequestError, OpenAI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate canonical semantic JSON and solvable JSON from an SVG via OpenAI API."
        )
    )
    parser.add_argument("--image", required=True, help="Path to input SVG image")
    parser.add_argument("--problem-id", required=True, help="problem_id to inject")
    parser.add_argument(
        "--semantic-schema-file",
        default="schema/semantic/semantic.v1.json",
        help="Path to canonical semantic schema",
    )
    parser.add_argument(
        "--solvable-schema-file",
        default="schema/solvable/solvable.v1.json",
        help="Path to solvable schema",
    )
    parser.add_argument(
        "--out-dir",
        default="modu_math/json_from_svg/contract_math",
        help="Output directory for generated JSON artifacts",
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


def load_svg_text(image_path: Path) -> str:
    return image_path.read_text(encoding="utf-8-sig")


def ensure_semantic_confidence_fields(
    payload: dict, default_confidence: float = 0.5
) -> None:
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


def enrich_semantic_answer_from_solvable(semantic: dict, solvable: dict) -> dict:
    sol_answer = solvable.get("answer")
    if not isinstance(sol_answer, dict):
        return semantic
    if "value" not in sol_answer:
        return semantic

    answer = semantic.get("answer")
    if not isinstance(answer, dict):
        answer = {}
        semantic["answer"] = answer

    if "value" not in answer:
        answer["value"] = sol_answer.get("value")
        answer.setdefault("source", "filled_from_solvable")

    if "unit" not in answer and isinstance(sol_answer.get("unit"), str):
        answer["unit"] = sol_answer["unit"]

    return semantic


def should_apply_ratio_override(problem_type: str) -> bool:
    pt = problem_type.lower()
    keywords = ("pie", "proportion", "ratio", "circle_graph", "circle-graph")
    return any(k in pt for k in keywords)


def extract_numeric_semantic_answer(semantic: dict) -> int | float | None:
    answer = semantic.get("answer")
    if not isinstance(answer, dict):
        return None

    value = answer.get("value")
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        try:
            num = float(stripped)
            return int(num) if abs(num - round(num)) < 1e-9 else num
        except ValueError:
            return None
    return None


def generate_with_schema(
    client: OpenAI,
    model: str,
    schema_name: str,
    schema: dict,
    system_text: str,
    user_instructions: str,
    svg_text: str,
    fallback_appendix: str | None = None,
) -> dict:
    base_input = [
        {
            "role": "system",
            "content": [{"type": "input_text", "text": system_text}],
        },
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": user_instructions},
                {
                    "type": "input_text",
                    "text": (
                        "Use the following SVG source as the only visual input.\n"
                        "<svg_source>\n"
                        f"{svg_text}\n"
                        "</svg_source>"
                    ),
                },
            ],
        },
    ]

    if fallback_appendix:
        base_input.append(
            {
                "role": "user",
                "content": [{"type": "input_text", "text": fallback_appendix}],
            }
        )

    try:
        response = client.responses.create(
            model=model,
            input=base_input,
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": to_openai_strict_schema(schema),
                }
            },
        )
        return json.loads(response.output_text)
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
        return json.loads(response.output_text)


def generate_semantic(
    client: OpenAI,
    model: str,
    semantic_schema: dict,
    svg_text: str,
    problem_id: str,
    image_path: Path,
) -> dict:
    payload = generate_with_schema(
        client=client,
        model=model,
        schema_name="modu_math_semantic_v1",
        schema=semantic_schema,
        system_text=(
            "You generate strict canonical JSON for Korean math worksheet parsing. "
            "Return only a JSON object that satisfies the given schema."
        ),
        user_instructions=(
            "Create canonical semantic JSON from this SVG. "
            f"Set `problem_id` to `{problem_id}` exactly. "
            "Include confidence fields for domain.objects, domain.relations, and answer. "
            "Use conservative confidence values when uncertain."
        ),
        svg_text=svg_text,
    )

    payload["problem_id"] = problem_id
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        payload["metadata"] = metadata
    metadata.setdefault("source_type", "svg")
    metadata.setdefault("source_path", str(image_path))
    ensure_semantic_confidence_fields(payload, default_confidence=0.5)

    Draft202012Validator(semantic_schema).validate(payload)
    return payload


def generate_solvable(
    client: OpenAI,
    model: str,
    solvable_schema: dict,
    semantic_payload: dict,
    svg_text: str,
    problem_id: str,
) -> dict:
    payload = generate_with_schema(
        client=client,
        model=model,
        schema_name="modu_math_solvable_v1",
        schema=solvable_schema,
        system_text=(
            "You generate strict solvable JSON for Korean math problems. "
            "Return only a JSON object that satisfies the given schema."
        ),
        user_instructions=(
            "Create solvable JSON from this SVG and semantic context. "
            f"Set `problem_id` to `{problem_id}` exactly. "
            "Set `schema` to `modu.solvable.v1` exactly. "
            "Important: `total_ticks` means the count of physical tick marks around the chart, "
            "not the numeric labels such as 0/25/50/75. "
            "For pie-chart tick problems, count the short tick lines and sector span in tick units. "
            "Write Korean explanations in `plan`, and if possible include "
            "`description_ko`/`formula_ko` in steps and `explanation_ko` in answer. "
            "Ensure arithmetic is correct and checks are internally consistent.\n\n"
            "Semantic context:\n"
            + json.dumps(semantic_payload, ensure_ascii=False, separators=(",", ":"))
        ),
        svg_text=svg_text,
    )

    payload["schema"] = "modu.solvable.v1"
    payload["problem_id"] = problem_id
    if "problem_type" not in payload and "problem_type" in semantic_payload:
        payload["problem_type"] = semantic_payload["problem_type"]
    if isinstance(payload.get("answer"), dict):
        answer = payload["answer"]
        if "unit" not in answer:
            answer["unit"] = "\uBA85"

    # Deterministic arithmetic post-processing only for ratio/pie problems.
    inputs = payload.get("inputs")
    answer = payload.get("answer")
    semantic_pt = semantic_payload.get("problem_type")
    payload_pt = payload.get("problem_type")
    resolved_pt = str(payload_pt or semantic_pt or "")
    apply_ratio_override = should_apply_ratio_override(resolved_pt)

    if apply_ratio_override and isinstance(inputs, dict) and isinstance(answer, dict):
        total_ticks = inputs.get("total_ticks")
        target_ticks = inputs.get("target_ticks")
        target_count = inputs.get("target_count")
        if (
            isinstance(total_ticks, (int, float))
            and isinstance(target_ticks, (int, float))
            and isinstance(target_count, (int, float))
            and float(target_ticks) != 0.0
        ):
            derived_total = float(target_count) * float(total_ticks) / float(target_ticks)
            if abs(derived_total - round(derived_total)) < 1e-9:
                derived_total = int(round(derived_total))
            answer["value"] = derived_total
            if isinstance(inputs.get("unit"), str) and inputs["unit"].strip():
                answer["unit"] = inputs["unit"]

            checks = payload.get("checks")
            if isinstance(checks, list) and checks:
                first_check = checks[0]
                if isinstance(first_check, dict):
                    actual = float(derived_total) * float(target_ticks) / float(total_ticks)
                    if abs(actual - round(actual)) < 1e-9:
                        actual = int(round(actual))
                    first_check["expected"] = target_count
                    first_check["actual"] = actual
                    first_check["pass"] = actual == target_count
    else:
        # For non-ratio problems, prefer semantic answer when available.
        semantic_answer_num = extract_numeric_semantic_answer(semantic_payload)
        if semantic_answer_num is not None and isinstance(answer, dict):
            answer["value"] = semantic_answer_num

    Draft202012Validator(solvable_schema).validate(payload)
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
    if image_path.suffix.lower() != ".svg":
        raise ValueError("Only SVG is supported in this script. Use a .svg file.")

    semantic_schema_path = Path(args.semantic_schema_file).resolve()
    if not semantic_schema_path.exists():
        raise FileNotFoundError(
            f"Semantic schema file not found: {semantic_schema_path}"
        )
    semantic_schema = load_json(semantic_schema_path)

    solvable_schema_path = Path(args.solvable_schema_file).resolve()
    if not solvable_schema_path.exists():
        raise FileNotFoundError(
            f"Solvable schema file not found: {solvable_schema_path}"
        )
    solvable_schema = load_json(solvable_schema_path)

    model = args.model or os.getenv("OPENAI_MODEL") or "gpt-5.4-mini"
    client = OpenAI()
    svg_text = load_svg_text(image_path)

    semantic = generate_semantic(
        client=client,
        model=model,
        semantic_schema=semantic_schema,
        svg_text=svg_text,
        problem_id=args.problem_id,
        image_path=image_path,
    )
    solvable = generate_solvable(
        client=client,
        model=model,
        solvable_schema=solvable_schema,
        semantic_payload=semantic,
        svg_text=svg_text,
        problem_id=args.problem_id,
    )
    semantic = enrich_semantic_answer_from_solvable(semantic, solvable)
    Draft202012Validator(semantic_schema).validate(semantic)

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = args.output_prefix or args.problem_id
    semantic_out_path = out_dir / f"{prefix}.semantic.contract.v1.json"
    solvable_out_path = out_dir / f"{prefix}.solvable.v1.json"

    semantic_out_path.write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    solvable_out_path.write_text(
        json.dumps(solvable, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Generated canonical semantic JSON: {semantic_out_path}")
    print(f"Generated solvable JSON: {solvable_out_path}")


if __name__ == "__main__":
    main()
