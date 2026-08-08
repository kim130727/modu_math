from __future__ import annotations

import os
import sys


def main(argv: list[str] | None = None) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv if argv is None else argv)
