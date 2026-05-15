from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
SECRET_KEY = os.environ.get("MODU_MATH_WEB_SECRET_KEY", "dev-secret-key")
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "modu_math_web.urls"
MIDDLEWARE: list[str] = []
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "modu_math_web.editor",
]
TEMPLATES: list[dict] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src" / "modu_math_web" / "editor" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
        },
    }
]
WSGI_APPLICATION = "modu_math_web.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
PROBLEMS_ROOT = Path(os.environ.get("MODU_PROBLEMS_ROOT", BASE_DIR / "examples" / "problems"))
