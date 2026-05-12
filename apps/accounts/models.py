from django.db import models
from django.contrib.auth.models import AbstractUser


class UserType(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"
    STAFF = "staff", "Staff"
    OWNER = "owner", "Owner"


class UserGender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    full_name = models.CharField(
        max_length=255,
        default="John Doe"
    )

    # use inherited email field from AbstractUser
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )

    gender = models.CharField(
        max_length=10,
        choices=UserGender.choices,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.full_name