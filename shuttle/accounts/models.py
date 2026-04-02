import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("owner", "Owner"),
        ("driver", "Driver"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} -{self.role}"


#creating verification model


class Driverprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile"

                                )
    address = models.TextField(
        max_length=200,
        blank=True
    )

    license_number = models.CharField(
        max_length=100,
        blank=True
    )

    license_upload = models.FileField(
        upload_to="drivers/licenses/",
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profiles',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class DriverApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    driver = models.ForeignKey(

        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )

    experience_years = models.IntegerField()
    reason = models.TextField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending"
                              )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):
        return f" {self.driver} - {self.status}"


#creating a bus model 


class Bus(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),

    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="buses"
    )
    driver = models.OneToOneField(
        Driverprofile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_bus"
    )
    vehicle_name = models.CharField(max_length=200, null=True)
    plate_no = models.CharField(max_length=100, null=True)
    colour = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    image = models.ImageField(upload_to="bus_images/", blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.vehicle_name} - {self.plate_no}"


class ComplaintTicket(models.Model):
    STATUS_CHOICES = (
        ("open", "OPEN"),
        ("in_progress", "IN_PROGRESS"),
        ("closed", "CLOSED"),
    )

    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.user.username} - {self.subject}"


class ComplaintMessage(models.Model):
    ticket = models.ForeignKey(
        ComplaintTicket,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender =models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='complaints/attachments/',
    blank=True,
    null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.sender.username} - {self.ticket.subject}"