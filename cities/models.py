from django.db import models
from states.models import State


class City(models.Model):

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="cities"
    )

    name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name} ({self.state.name})"