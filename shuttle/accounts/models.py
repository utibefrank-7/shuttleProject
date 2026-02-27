from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    ROLE_CHOICES =(
        ("admin", "Admin"),
        ("owner", "Owner"),
        ("driver", "Driver"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} -{self.role}"


