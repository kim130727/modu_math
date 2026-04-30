"""Project-local tools package used by test imports.

This file makes `tools` an explicit package so imports like:
    from tools import batch_generate_dsl
    from tools.generate_dsl_from_png import ...
work reliably under pytest collection.
"""

