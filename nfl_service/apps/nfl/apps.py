"""nfl app configuration."""

from django.apps import AppConfig


class nflConfig(AppConfig):
    """nfl application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nfl"
    verbose_name = "nfl"
