"""One authored JSON document per Korean source; legacy sidecars remain readable."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading

LANGUAGES = frozenset({"ko", "en", "ja", "zh", "uk", "km"})
SUFFIX = ".i18n.json"
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


def document_path(canonical: Path) -> Path:
    return canonical.with_name(canonical.name.removesuffix(".dsl.py") + SUFFIX)


def read_document(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("version") != 2 or data.get("source_language") != "ko":
        raise ValueError(f"Unsupported problem document: {path}")
    return data


def consolidated(path: Path) -> bool:
    info = location(path)
    if info is None:
        return False
    canonical, language, _ = info
    document = document_path(canonical)
    if not document.is_file():
        return False
    return language == "ko" or language in read_document(document).get("languages", {})


@contextmanager
def file_lock(path: Path):
    """Cross-process lock, reentrant within a thread (Windows and POSIX)."""
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
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
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
    """Small text-document interface used by legacy authoring services."""
    def __init__(self, document: Path, keys: tuple[str, ...], root: Path):
        self.document, self.keys, self.root = document, keys, root
        self._observed = None

    def _value(self):
        value = read_document(self.document)
        for key in self.keys:
            value = value[key]
        return value

    def exists(self):
        try:
            self._value()
            return True
        except (FileNotFoundError, KeyError):
            return False

    is_file = exists

    def read_text(self, encoding="utf-8"):
        value = self._value()
        self._observed = json.dumps(value, sort_keys=True, ensure_ascii=False)
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"

    def write_text(self, text, encoding="utf-8", **kwargs):
        value = json.loads(text)
        digest = hashlib.sha256(str(self.document).encode()).hexdigest()
        with file_lock(self.root / ".modu-cache" / "locks" / (digest + ".lock")):
            data = read_document(self.document)
            parent = data
            for key in self.keys[:-1]:
                parent = parent.setdefault(key, {})
            if self._observed is not None and json.dumps(parent.get(self.keys[-1]), sort_keys=True, ensure_ascii=False) != self._observed:
                raise ValueError("This language was edited concurrently; reload before saving")
            parent[self.keys[-1]] = value
            atomic_write(self.document, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())
            self._observed = json.dumps(value, sort_keys=True, ensure_ascii=False)
        return len(text)

    def __str__(self):
        return f"{self.document}#{'/'.join(self.keys)}"


def section(path: Path, name: str) -> JsonSection | None:
    if not consolidated(path):
        return None
    canonical, language, root = location(path)
    keys = (name,) if language == "ko" else ("languages", language, name)
    return JsonSection(document_path(canonical), keys, root)


def virtual_paths(root: Path):
    for document in sorted((root / "ko").rglob("*" + SUFFIX)):
        canonical = document.with_name(document.name.removesuffix(SUFFIX) + ".dsl.py")
        relative = canonical.relative_to(root / "ko")
        for language in read_document(document).get("languages", {}):
            if language not in LANGUAGES or language == "ko":
                raise ValueError(f"Unsupported language: {language}")
            yield root / language / relative
