"""Build the assignment-only Flutter app without packaging authored answers."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[3]
APP = REPO / "apps/mobile"
OUTPUT = REPO / "src/modu_math_web/editor_next/static/editor_next/student_app"


def prepare_project(source: Path, stage: Path) -> None:
    stage.mkdir(parents=True, exist_ok=True)
    for folder in ("lib", "web", "assets/i18n", "assets/characters"):
        shutil.copytree(source / folder, stage / folder)
    for name in ("pubspec.lock", "analysis_options.yaml"):
        if (source / name).is_file():
            shutil.copy2(source / name, stage / name)
    pubspec = (source / "pubspec.yaml").read_text(encoding="utf-8")
    pubspec = (
        "\n".join(
            line
            for line in pubspec.splitlines()
            if not line.strip().startswith("- generated/")
        )
        + "\n"
    )
    (stage / "pubspec.yaml").write_text(pubspec, encoding="utf-8")


def verify_bundle(output: Path) -> None:
    for file in output.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(output).as_posix()
        if (
            "generated/examples" in relative
            or file.name.endswith(
                (".dsl.py", ".renderer.json", ".semantic.json", ".layout.json")
            )
            or ".solvable." in file.name
        ):
            raise RuntimeError(
                f"Private problem artifact in student output: {relative}"
            )
    if not (output / "main.dart.js").is_file():
        raise RuntimeError("Student JavaScript bundle is missing")


def stamp_web_cache_bust(output: Path) -> None:
    bundle = output / "main.dart.js"
    version = hashlib.sha256(bundle.read_bytes()).hexdigest()[:12]
    bootstrap = output / "flutter_bootstrap.js"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        text = text.replace('"mainJsPath":"main.dart.js"', f'"mainJsPath":"main.dart.js?v={version}"')
        bootstrap.write_text(text, encoding="utf-8")
    index = output / "index.html"
    if index.is_file():
        html = index.read_text(encoding="utf-8")
        html = html.replace('src="flutter_bootstrap.js"', f'src="flutter_bootstrap.js?v={version}"')
        index.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", default="same-origin")
    options = parser.parse_args()
    flutter = shutil.which("flutter")
    if flutter is None:
        raise SystemExit("Flutter is not on PATH")
    scratch = REPO / ".tmp/student-build"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="project-", dir=scratch) as directory:
        stage = Path(directory).resolve()
        assert stage.is_relative_to(scratch.resolve())
        prepare_project(APP, stage)
        subprocess.run([flutter, "pub", "get"], cwd=stage, check=True)
        subprocess.run(
            [
                flutter,
                "build",
                "web",
                "--release",
                "--pwa-strategy=none",
                "--no-wasm-dry-run",
                "--target",
                "lib/main.dart",
                "--base-href",
                "/static/editor_next/student_app/",
                "--output",
                str(OUTPUT),
                f"--dart-define=BACKEND_API_BASE_URL={options.backend}",
            ],
            cwd=stage,
            check=True,
        )
    stamp_web_cache_bust(OUTPUT)
    verify_bundle(OUTPUT)
    print(f"Student bundle verified: {OUTPUT}")


if __name__ == "__main__":
    main()
