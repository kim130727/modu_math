"""Consolidate authored JSON, verify all renders, then optionally remove sidecars."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from modu_math.dsl.problem_store import atomic_write, document_path, SUFFIX
from modu_math_web.editor.services.problems import ProblemPaths


def paths_for(root, dsl):
    return ProblemPaths(dsl.relative_to(root).as_posix(), "", root,
                        dsl.parent, dsl, dsl.name.removesuffix(".dsl.py"))


def consolidate_provenance(root: Path, *, delete=False):
    """Preserve old source metadata and diagnostic reports in the same document."""
    from modu_math.dsl.problem_store import read_document, JsonSection
    root = root.resolve()
    candidates = []
    for document in (root / "ko").rglob("*" + SUFFIX):
        data = read_document(document)
        prefix = document.name.removesuffix(SUFFIX)
        relative_dir = document.parent.relative_to(root / "ko")
        for language in ["ko", *data.get("languages", {})]:
            directory = root / language / relative_dir
            files = sorted(set(directory.glob(prefix + ".*.json")) | set(directory.glob(prefix + ".json")))
            files = [path for path in files if path != document]
            if not files:
                continue
            keys = ("provenance",) if language == "ko" else ("languages", language, "provenance")
            stored = JsonSection(document, keys, root)
            payload = json.loads(stored.read_text()) if stored.exists() else {}
            for path in files:
                name = path.name.removeprefix(prefix)
                value = json.loads(path.read_text(encoding="utf-8-sig"))
                if name in payload and payload[name] != value:
                    raise ValueError(f"Conflicting archived metadata: {path}")
                payload[name] = value
                candidates.append(path)
            stored.write_text(json.dumps(payload, ensure_ascii=False))
            assert json.loads(stored.read_text()) == payload
    if delete:
        for path in candidates:
            if root not in path.resolve().parents:
                raise ValueError(f"Outside migration root: {path}")
        for path in candidates:
            path.unlink()
    return len(candidates)


def consolidate(root: Path, *, catalogs: Path | None = None, delete=False):
    from modu_math_web.editor.services.build import compile_problem_artifacts
    from modu_math_web.editor.services.artifact_cache import get_artifacts
    root = root.resolve()
    pending_delete = set()
    verified = []
    documents = []
    for canonical in sorted((root / "ko").rglob("*.dsl.py")):
        output = document_path(canonical)
        if output.exists():
            raise ValueError(f"Already consolidated: {output}; refusing to overwrite edits")
        prefix = canonical.name.removesuffix(".dsl.py")
        authored = {"version": 2, "source_language": "ko", "editor_overrides": {}, "languages": {}}
        language_paths = [canonical]
        relative = canonical.relative_to(root / "ko")
        for language in ("uk",):
            virtual = root / language / relative
            delta = virtual.with_name(prefix + ".locale-delta.json")
            if delta.exists():
                authored["languages"][language] = {"delta": json.loads(delta.read_text(encoding="utf-8"))}
                language_paths.append(virtual)
                pending_delete.add(delta)
        baseline = {}
        for dsl in language_paths:
            language = dsl.relative_to(root).parts[0]
            overrides = dsl.with_name(prefix + ".editor_overrides.json")
            # Compile first: the pipeline may normalize old override records.
            baseline[language] = compile_problem_artifacts(paths_for(root, dsl))
            record = authored if language == "ko" else authored["languages"][language]
            record["editor_overrides"] = json.loads(overrides.read_text(encoding="utf-8-sig")) if overrides.exists() else {}
            if overrides.exists():
                pending_delete.add(overrides)
            if catalogs:
                matches = [path for path in (catalogs / language).glob("*.locale.json")
                           if path.name.removesuffix(".locale.json").replace("_초등_", "_elem_") == prefix]
                if len(matches) > 1:
                    raise ValueError(f"Ambiguous translation catalog: {prefix}/{language}")
                if matches:
                    record["translation_catalog"] = json.loads(matches[0].read_text(encoding="utf-8-sig"))
                    pending_delete.add(matches[0].resolve())
            for suffix in (".semantic.json", ".layout.json", ".renderer.json", ".svg", ".solvable.json",
                           ".solvable.v1.json", ".solvable.v1.1.json", ".solvable.v1.2.json", ".solvable.v1.3.json"):
                artifact = dsl.with_name(prefix + suffix)
                if artifact.exists():
                    pending_delete.add(artifact)
        atomic_write(output, (json.dumps(authored, ensure_ascii=False, indent=2) + "\n").encode())
        try:
            for dsl in language_paths:
                language = dsl.relative_to(root).parts[0]
                rendered = get_artifacts(paths_for(root, dsl), force=True)
                if rendered != baseline[language]:
                    raise ValueError(f"Rendered data changed during consolidation: {dsl}")
                verified.append(dsl.relative_to(root).as_posix())
        except Exception:
            output.unlink()  # This command created it; all legacy input is still intact.
            raise
        documents.append(output)
    before_bytes = sum(path.stat().st_size for path in pending_delete)
    after_bytes = sum(path.stat().st_size for path in documents)
    if delete:
        allowed = [root] + ([catalogs.resolve()] if catalogs else [])
        for path in pending_delete:
            if not any(parent in path.resolve().parents for parent in allowed):
                raise ValueError(f"Refusing to delete outside migration roots: {path}")
        for path in sorted(pending_delete):
            path.unlink()
    return {"documents": len(documents), "verified_renders": len(verified),
            "removed_files": len(pending_delete) if delete else 0,
            "old_bytes": before_bytes, "authored_json_bytes": after_bytes}


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
    import django
    django.setup()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--catalogs", type=Path)
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()
    print(consolidate(args.root, catalogs=args.catalogs, delete=args.delete))
