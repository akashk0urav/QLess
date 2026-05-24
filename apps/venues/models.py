from django.db import models

class Category(models.TextChoices):
    RESTAURANT = "restaurant", "Restaurant"
    BAR = "bar", "Bar"
    CAFE = "cafe", "Cafe"
    SALON = "salon", "Salon"
    GYM = "gym", "Gym"
    CLINIC = "clinic", "Clinic"
    OTHER = "other", "Other"

# represents a business that customers can join a queue for. Examples include restaurants, salons, clinics, etc.


class Venue(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_queue_open = models.BooleanField(default=False)
    is_venue_verified = models.BooleanField(default=False)
    average_service_time_per_customer_minutes = models.PositiveIntegerField(default=15)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
    

class VenueMember(models.Model):

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        STAFF = "staff", "Staff"

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="venue_memberships"
    )

    role = models.CharField(max_length=20, choices=Role.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "user"],
                name="unique_venue_user"
            )
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.venue.name}"