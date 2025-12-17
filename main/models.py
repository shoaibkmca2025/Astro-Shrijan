from django.conf import settings
from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending_payment", "pending_payment"),
        ("confirmed", "confirmed"),
        ("cancelled", "cancelled"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    time = models.TimeField(null=True, blank=True)
    place = models.CharField(max_length=200, blank=True)
    questions = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending_payment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} - {self.name}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "pending"),
        ("succeeded", "succeeded"),
        ("failed", "failed"),
        ("cancelled", "cancelled"),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    provider = models.CharField(max_length=50, default="test")
    provider_order_id = models.CharField(max_length=120, blank=True)
    reference = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.status}"
