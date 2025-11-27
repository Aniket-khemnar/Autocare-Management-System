from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

User = settings.AUTH_USER_MODEL


class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('general', 'General Service'),
        ('oil_change', 'Oil Change'),
        ('repair', 'Repair'),
        ('custom', 'Custom Request'),
    ]

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='bookings'
    )
    mechanic = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_bookings'
    )
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    preferred_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.registration_no} - {self.service_type} ({self.status})"
