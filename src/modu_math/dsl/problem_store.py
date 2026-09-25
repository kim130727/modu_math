"""Storage paths for canonical Korean problems and split localization data."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading

LANGUAGES = frozenset({"ko", "uk"})
SUFFIX = ".i18n.json"  # Legacy migration input only.
_locks: dict[str, threading.RLock] = {}
_guard = threading.Lock()
_held = threading.local()


def location(path: Path) -> tuple[Path, str, Path] | None:
    path = path.resolve()
    for parent in path.parents:
        if parent.name in LANGUAGES:
            relative = path.relative_to(parent)
            canonical = parent.parent / "ko" / relative
            return canonical, parent.name, parent.parent
    return None


def repository_root(problem_root: Path) -> Path:
    problem_root = problem_root.resolve()
    for candidate in (problem_root, *problem_root.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    return problem_root.parent


def _relative_json(canonical: Path, root: Path) -> Path:
    relative = canonical.relative_to(root / "ko")
    return relative.with_name(relative.name.removesuffix(".dsl.py") + ".json")


def locale_path(path: Path, language: str | None = None) -> Path:
    info = location(path)
    if info is None:
        raise ValueError(f"Problem path is not under a language directory: {path}")
    canonical, detected, root = info
    target = language or detected
    return repository_root(root) / "locales" / target / _relative_json(canonical, root)


def override_path(path: Path, language: str | None = None) -> Path:
    info = location(path)
    if info is None:
        raise ValueError(f"Problem path is not under a language directory: {path}")
    canonical, detected, root = info
    target = language or detected
    relative = _relative_json(canonical, root)
    return repository_root(root) / "overrides" / target / relative.with_suffix(".layout.json")


def review_path(path: Path, language: str | None = None) -> Path:
    return override_path(path, language).with_suffix(".review.json")


def document_path(canonical: Path) -> Path:
    """Return the old integrated path for migration tooling only."""
    return canonical.with_name(canonical.name.removesuffix(".dsl.py") + SUFFIX)


def read_document(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("version") != 2 or data.get("source_language") != "ko":
        raise ValueError(f"Unsupported legacy problem document: {path}")
    return data


def consolidated(path: Path) -> bool:
    """Compatibility name: true when a problem uses managed localization storage."""
    info = location(path)
    if info is None:
        return False
    canonical, language, _ = info
    if language == "ko" and any(locale_path(canonical, target).is_file() for target in LANGUAGES - {"ko"}):
        return True
    if language != "ko" and locale_path(canonical, language).is_file():
        return True
    legacy = document_path(canonical)
    if legacy.is_file():
        return language == "ko" or language in read_document(legacy).get("languages", {})
    return False


@contextmanager
def file_lock(path: Path):
    key = str(path.resolve())
    with _guard:
        lock = _locks.setdefault(key, threading.RLock())
    with lock:
        held = getattr(_held, "keys", set())
        if key in held:
            yield
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a+b") as stream:
            stream.seek(0, os.SEEK_END)
            if stream.tell() == 0:
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            _held.keys = held | {key}
            try:
                yield
            finally:
                _held.keys = held
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".writing-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class JsonSection:
    """Path-like JSON section with optimistic concurrency checks."""
    def __init__(self, document: Path, keys: tuple[str, ...], root: Path, defaults: dict | None = None):
        self.document, self.keys, self.root = document, keys, root
        self.defaults = defaults or {}
        self._observed = None

    def _document_value(self):
        if not self.document.exists():
            return json.loads(json.dumps(self.defaults))
        return json.loads(self.document.read_text(encoding="utf-8-sig"))

    def _value(self):
        value = self._document_value()
        for key in self.keys:
            value = value[key]
        return value

    def exists(self):
        try:
            self._value()
            return self.document.exists()
        except (FileNotFoundError, KeyError):
            return False

    is_file = exists

    def read_text(self, encoding="utf-8"):
        value = self._value()
        self._observed = json.dumps(value, sort_keys=True, ensure_ascii=False)
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"

    def read_bytes(self):
        return self.read_text().encode("utf-8")

    def write_text(self, text, encoding="utf-8", **kwargs):
        value = json.loads(text)
        digest = hashlib.sha256(str(self.document).encode()).hexdigest()
        with file_lock(self.root / ".modu-cache" / "locks" / (digest + ".lock")):
            data = self._document_value()
            parent = data
            for key in self.keys[:-1]:
                parent = parent.setdefault(key, {})
            current = parent.get(self.keys[-1]) if self.keys else data
            if self._observed is not None and json.dumps(current, sort_keys=True, ensure_ascii=False) != self._observed:
                raise ValueError("This language was edited concurrently; reload before saving")
            if self.keys:
                parent[self.keys[-1]] = value
            else:
                data = value
            atomic_write(self.document, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())
            self._observed = json.dumps(value, sort_keys=True, ensure_ascii=False)
        return len(text)

    def write_bytes(self, content: bytes):
        return self.write_text(content.decode("utf-8"))

    def __str__(self):
        return f"{self.document}#{'/'.join(self.keys)}"


def section(path: Path, name: str) -> JsonSection | None:
    info = location(path)
    if info is None:
        return None
    canonical, language, root = info
    legacy = document_path(canonical)
    using_split = language != "ko" and locale_path(path, language).is_file()
    using_split = using_split or (
        language == "ko"
        and any(locale_path(canonical, target).is_file() for target in LANGUAGES - {"ko"})
    )
    if legacy.is_file() and not using_split:
        keys = (name,) if language == "ko" else ("languages", language, name)
        return JsonSection(legacy, keys, root)
    if name == "translation_catalog" and language != "ko":
        target = locale_path(path, language)
        defaults = {
            "version": 1,
            "problem_id": canonical.name.removesuffix(".dsl.py"),
            "source_language": "ko",
            "target_language": language,
            "strings": {},
        }
        return JsonSection(target, ("strings",), root, defaults)
    if name == "editor_overrides" and (using_split or override_path(path, language).is_file()):
        return JsonSection(override_path(path, language), (), root, {"version": 1})
    if name == "review" and language != "ko" and locale_path(path, language).is_file():
        return JsonSection(review_path(path, language), (), root, {})
    return None


def virtual_paths(root: Path):
    seen = set()
    legacy_documents = sorted((root / "ko").rglob("*" + SUFFIX))
    for document in legacy_documents:
        canonical = document.with_name(document.name.removesuffix(SUFFIX) + ".dsl.py")
        relative = canonical.relative_to(root / "ko")
        for language in read_document(document).get("languages", {}):
            target = root / language / relative
            seen.add(target)
            yield target
    base = repository_root(root) / "locales"
    for language in LANGUAGES - {"ko"}:
        language_root = base / language
        if not language_root.exists():
            continue
        for catalog in sorted(language_root.rglob("*.json")):
            relative = catalog.relative_to(language_root)
            target = root / language / relative.with_name(relative.stem + ".dsl.py")
            if target not in seen:
                yield target
