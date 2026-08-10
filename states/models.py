from django.db import models
from countries.models import Country


class State(models.Model):

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states"
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    capital = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return f"{self.name} ({self.country.name})"