from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from modu_semantic.rag.logger import append_run_log
from modu_semantic.rag.meta_recommender import recommend_input_meta, tune_meta_from_ocr_features
from modu_semantic.rag.ocr import extract_ocr_features, merge_ocr_result_into_meta
from modu_semantic.rag.pipeline import (
    build_generation_scaffold,
    make_run_id,
    persist_generated_outputs,
    validate_generated_python,
)
from modu_semantic.rag.prompt_builder import build_few_shot_prompt
from modu_semantic.rag.retrieve import retrieve_examples


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or "rag"


def _load_input_meta(*, meta_json: str | None, meta_path: str | None) -> dict[str, Any] | None:
    if meta_json:
        payload = json.loads(meta_json)
        if not isinstance(payload, dict):
            raise ValueError("--meta-json must decode to an object")
        return payload

    if meta_path:
        payload = json.loads(Path(meta_path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("--meta-path content must be a JSON object")
        return payload

    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run retrieval + few-shot prompt generation + local validation scaffold")
    parser.add_argument("--meta-json", default=None, help="Input metadata as JSON object string")
    parser.add_argument("--meta-path", default=None, help="Path to JSON file containing input metadata")
    parser.add_argument("--image-path", default=None, help="Optional input image path for OCR preprocessing and meta recommendation")
    parser.add_argument("--index-path", default="examples/problem/_rag/index.jsonl")
    parser.add_argument("--examples-root", default="examples/problem")
    parser.add_argument("--runs-path", default="examples/problem/_rag/runs.jsonl")
    parser.add_argument("--output-dir", default="examples/problem/_rag/generated")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument(
        "--disable-ocr",
        action="store_true",
        help="Disable OCR preprocessing even when --image-path is provided.",
    )
    parser.add_argument(
        "--artifact-prefix",
        default=None,
        help="Optional readable file prefix for generated artifacts (default: problem_id if provided).",
    )
    parser.add_argument(
        "--generated-py-path",
        default=None,
        help="Optional existing generated .py file to validate. If omitted, scaffold file is validated.",
    )
    parser.add_argument(
        "--persist-output",
        action="store_true",
        help="Persist semantic/layout/svg outputs next to generated artifacts when validation succeeds.",
    )
    args = parser.parse_args(argv)

    explicit_meta = _load_input_meta(meta_json=args.meta_json, meta_path=args.meta_path)
    if explicit_meta is None and not args.image_path:
        raise ValueError("Either --meta-json/--meta-path or --image-path is required")

    input_meta = recommend_input_meta(
        explicit_meta=explicit_meta,
        index_path=args.index_path,
        image_path=args.image_path,
    )

    ocr_status = "skipped"
    ocr_error = ""
    if args.image_path and not args.disable_ocr:
        ocr_result = extract_ocr_features(args.image_path)
        input_meta = merge_ocr_result_into_meta(input_meta, ocr_result)
        input_meta = tune_meta_from_ocr_features(input_meta)
        if ocr_result.available:
            ocr_status = "ok"
        else:
            ocr_status = "unavailable"
            ocr_error = ocr_result.error

    run_id = make_run_id()
    problem_id = str(input_meta.get("problem_id") or "").strip()
    readable_prefix = args.artifact_prefix or (problem_id if problem_id else run_id)
    artifact_prefix = _slug(readable_prefix)

    retrieved = retrieve_examples(input_meta, index_path=args.index_path, top_k=args.top_k)
    prompt = build_few_shot_prompt(
        input_meta=input_meta,
        retrieved_examples=retrieved,
        examples_root=args.examples_root,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = output_dir / f"{artifact_prefix}.prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    scaffold_py_path = build_generation_scaffold(
        output_dir=output_dir,
        run_id=run_id,
        input_meta=input_meta,
        file_stem=artifact_prefix,
    )

    target_py = Path(args.generated_py_path) if args.generated_py_path else scaffold_py_path
    build_success, validation_success, error_message = validate_generated_python(target_py)

    persisted_prefix: Path | None = None
    persisted_files: list[Path] = []
    if args.persist_output and build_success and validation_success:
        persisted_prefix = output_dir / f"{artifact_prefix}_built"
        persisted_ok, persisted_error = persist_generated_outputs(
            target_py,
            out_prefix=persisted_prefix,
            validate=True,
        )
        if not persisted_ok:
            validation_success = False
            error_message = persisted_error
        else:
            persisted_files = [
                output_dir / f"{artifact_prefix}_built.semantic.json",
                output_dir / f"{artifact_prefix}_built.svg",
            ]

    latest_files: list[str] = []
    if problem_id:
        latest_prefix = _slug(problem_id)
        latest_prompt = output_dir / f"{latest_prefix}.latest.prompt.txt"
        latest_generated = output_dir / f"{latest_prefix}.latest.generated.py"
        shutil.copyfile(prompt_path, latest_prompt)
        source_generated = target_py if target_py.exists() else scaffold_py_path
        shutil.copyfile(source_generated, latest_generated)
        latest_files.extend([str(latest_prompt), str(latest_generated)])

        if persisted_files and validation_success:
            latest_semantic = output_dir / f"{latest_prefix}.latest.semantic.json"
            latest_svg = output_dir / f"{latest_prefix}.latest.svg"
            shutil.copyfile(persisted_files[0], latest_semantic)
            shutil.copyfile(persisted_files[1], latest_svg)
            latest_files.extend([str(latest_semantic), str(latest_svg)])

    append_run_log(
        runs_path=args.runs_path,
        run_id=run_id,
        input_meta=input_meta,
        retrieved_examples=[str(item["entry"].get("problem_id")) for item in retrieved],
        generated_py_path=str(target_py),
        build_success=build_success,
        validation_success=validation_success,
        error_message=error_message,
    )

    print(f"run_id: {run_id}")
    print(f"prompt_path: {prompt_path}")
    print(f"scaffold_py_path: {scaffold_py_path}")
    print(f"target_py: {target_py}")
    print(f"build_success: {build_success}")
    print(f"validation_success: {validation_success}")
    if args.image_path:
        print(f"image_path: {args.image_path}")
        print(f"ocr_status: {ocr_status}")
        if ocr_error:
            print(f"ocr_error: {ocr_error}")
    if persisted_prefix is not None and validation_success:
        print(f"persisted_outputs_prefix: {persisted_prefix}")
    if latest_files:
        print("latest_aliases:")
        for path in latest_files:
            print(f"  - {path}")
    if error_message:
        print(f"error: {error_message}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
