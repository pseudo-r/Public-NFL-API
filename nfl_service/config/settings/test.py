"""Test settings."""

import os as _os

import environ as _environ

from .base import *  # noqa: E402, F401, F403

DEBUG = False

# Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Cache - Use dummy cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Celery - Always eager for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Logging - Reduce noise during tests
LOGGING["root"]["level"] = "WARNING"  # noqa: F405
for logger in LOGGING["loggers"].values():  # noqa: F405
    logger["level"] = "WARNING"

# Faster static files handling
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"}, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}

# nfl Client - Use test configuration
NFL_CLIENT = {
    "SITE_API_BASE_URL": "https://site.api.espn.com",
    "CORE_API_BASE_URL": "https://sports.core.api.espn.com",
    "TIMEOUT": 5.0,
    "MAX_RETRIES": 1,
    "RETRY_BACKOFF": 0.1,
    "USER_AGENT": "nfl-Service-Test/1.0",
    "RATE_LIMIT_REQUESTS": 1000,
    "RATE_LIMIT_PERIOD": 60,
}

# Opt into a separate test database explicitly; never use production DATABASE_URL.


if _os.environ.get("TEST_DATABASE_URL"):
    DATABASES = {"default": _environ.Env.db_url_config(_os.environ["TEST_DATABASE_URL"])}
MIDDLEWARE = [m for m in MIDDLEWARE if m != "whitenoise.middleware.WhiteNoiseMiddleware"]  # noqa: F405
INGEST_REQUIRE_STAFF = False
