import os
from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    role = os.getenv("DJANGO_SUPERUSER_ROLE", "admin")  # default to admin

    if not username or not password:
        return

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        if hasattr(user, 'role'):
            user.role = role  # ✅ use the variable

        if hasattr(user, 'is_verified'):
            user.is_verified = True

        user.save()
        print(f"Admin user '{username}' created successfully.")  # helpful log
    else:
        print(f"Admin user '{username}' already exists.")  # helpful log