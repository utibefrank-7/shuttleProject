from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import django
        from django.db import connection
        # Only run in production and when explicitly enabled
        if os.getenv("DJANGO_SUPERUSER_USERNAME"):
            try:
                # Check if tables exist before querying
                if 'accounts_customuser' in connection.introspection.table_names():
                    from .create_admin import create_admin
                    create_admin()
            except Exception:
                pass  # Silently skip if DB not ready
