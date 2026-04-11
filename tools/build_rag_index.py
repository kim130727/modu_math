from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from modu_semantic.rag.indexer import build_and_write_index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build RAG example index JSONL from examples/problem")
    parser.add_argument("--examples-root", default="examples/problem")
    parser.add_argument("--index-path", default="examples/problem/_rag/index.jsonl")
    args = parser.parse_args(argv)

    path = build_and_write_index(examples_root=args.examples_root, index_path=args.index_path)
    print(f"RAG index written: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
