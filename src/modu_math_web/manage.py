from __future__ import annotations

import os
import sys


def _prefer_entrypoint_reload() -> None:
    import __main__

    spec = getattr(__main__, "__spec__", None)
    if spec is not None and spec.name == "__main__" and not spec.parent:
        __main__.__spec__ = None


def main(argv: list[str] | None = None) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
    _prefer_entrypoint_reload()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv if argv is None else argv)


if __name__ == "__main__":
    main()
