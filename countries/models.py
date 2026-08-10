from django.db import models

class Meta:
    verbose_name = "Country"
    verbose_name_plural = "Countries"


class Country(models.Model):
    CONTINENTS = [
        ("Asia", "Asia"),
        ("Europe", "Europe"),
        ("North America", "North America"),
        ("South America", "South America"),
        ("Africa", "Africa"),
        ("Australia", "Australia"),
        ("Antarctica", "Antarctica"),
    ]

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)
    continent = models.CharField(max_length=30, choices=CONTINENTS)
    currency = models.CharField(max_length=50)
    flag = models.ImageField(upload_to="countries/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
