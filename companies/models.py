from django.db import models
from countries.models import Country
from states.models import State
from cities.models import City
from areas.models import Area


class Company(models.Model):

    name = models.CharField(max_length=150)

    logo = models.ImageField(
        upload_to="companies/logos/",
        blank=True,
        null=True
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE
    )

    address = models.TextField(blank=True)

    phone = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    website = models.URLField(blank=True)

    gst_number = models.CharField(max_length=30, blank=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name