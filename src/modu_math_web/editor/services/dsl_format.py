from __future__ import annotations


def format_dsl_source(source: str) -> str:
    """Format DSL Python source when the optional formatter is available."""
    if not source.strip():
        return source
    try:
        import black
    except Exception:
        return source
    try:
        mode = black.FileMode(line_length=100)
        formatted = black.format_str(source, mode=mode)
    except Exception:
        return source
    return formatted
