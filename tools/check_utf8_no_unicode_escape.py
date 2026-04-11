#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


UNICODE_ESCAPE_RE = re.compile(r"\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}")
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".svg",
    ".html",
    ".css",
    ".js",
    ".ts",
}


def staged_files() -> list[Path]:
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"]
    out = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
    files = []
    for line in out.splitlines():
        p = Path(line.strip())
        if not p:
            continue
        if p.suffix.lower() in TEXT_SUFFIXES and p.exists():
            files.append(p)
    return files


def main() -> int:
    bad_utf8: list[str] = []
    bad_escape: list[str] = []

    for path in staged_files():
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            bad_utf8.append(str(path))
            continue

        if UNICODE_ESCAPE_RE.search(text):
            bad_escape.append(str(path))

    if not bad_utf8 and not bad_escape:
        return 0

    print("[pre-commit] 검사 실패", file=sys.stderr)
    if bad_utf8:
        print("UTF-8이 아닌 파일:", file=sys.stderr)
        for p in bad_utf8:
            print(f"  - {p}", file=sys.stderr)
    if bad_escape:
        print(r"유니코드 이스케이프(\\uXXXX / \\xNN) 포함 파일:", file=sys.stderr)
        for p in bad_escape:
            print(f"  - {p}", file=sys.stderr)
    print("한글은 UTF-8 리터럴(직접 한글)로 작성하세요.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

