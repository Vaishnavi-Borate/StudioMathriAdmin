from django.db import models
from cities.models import City


class Area(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="areas"
    )

    name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name