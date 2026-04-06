from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Only run in production and when explicitly enabled
        if os.getenv("DJANGO_SUPERUSER_USERNAME"):
            from .create_admin import create_admin
            create_admin()