import os
from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    role = os.getenv("DJANGO_SUPERUSER_ROLE", "admin")

    if not username or not password:
        return

    try:
        # Delete existing admin and recreate with correct fields
        User.objects.filter(username=username).delete()

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=role,
            is_verified=True,
            is_active=True
        )
        user.save()
        print(f"Admin user '{username}' created successfully.")

    except Exception as e:
        print(f"Error creating admin: {str(e)}")