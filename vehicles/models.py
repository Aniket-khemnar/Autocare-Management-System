from django.conf import settings
from django.db import models

class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=20, unique=True)
    last_service_date = models.DateField(null=True, blank=True)
    mileage = models.IntegerField(default=0)
    next_service_due = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.registration_no} - {self.model}"
