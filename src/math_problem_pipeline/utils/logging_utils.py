"""Logging helpers."""

from __future__ import annotations

import logging


def setup_logger(name: str = "math_problem_pipeline", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a module logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
