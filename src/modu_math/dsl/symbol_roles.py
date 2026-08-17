from __future__ import annotations

import re


PROTECTED_SYMBOL_ROLES = {"symbol_label", "choice_marker"}

_HANGUL_CHOICE_MARKERS = "가나다라마바사아자차카타파하"
_JAMO_CHOICE_MARKERS = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
_CIRCLED_CHOICE_MARKERS = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
_MARKER_CHARS = (
    re.escape(_HANGUL_CHOICE_MARKERS)
    + re.escape(_JAMO_CHOICE_MARKERS)
    + re.escape(_CIRCLED_CHOICE_MARKERS)
)
_MARKER_TOKEN_RE = re.compile(
    rf"(?:[\(\[\{{]?[{_MARKER_CHARS}][\)\]\}}]?|[{re.escape(_CIRCLED_CHOICE_MARKERS)}])"
    rf"(?:[.)])?"
)


def infer_symbol_text_role(
    *,
    slot_id: str,
    text: str,
    style_role: str = "",
    semantic_role: str | None = None,
) -> str | None:
    if semantic_role:
        return semantic_role
    if not is_symbol_marker_text(text):
        return None
    marker_context = f"{slot_id} {style_role}".lower()
    if any(token in marker_context for token in ("choice", "choices", "option", "select")):
        return "choice_marker"
    return "symbol_label"


def is_protected_symbol_role(role: str | None) -> bool:
    return role in PROTECTED_SYMBOL_ROLES


def is_symbol_marker_text(text: str) -> bool:
    normalized = re.sub(r"\s+", "", text)
    if not normalized:
        return False
    if len(normalized) > 24:
        return False
    cursor = 0
    token_count = 0
    while cursor < len(normalized):
        match = _MARKER_TOKEN_RE.match(normalized, cursor)
        if match is None:
            return False
        cursor = match.end()
        token_count += 1
    return token_count > 0
