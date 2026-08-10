from django.db import models
from companies.models import Company
from categories.models import Category
from countries.models import Country
from states.models import State
from cities.models import City
from areas.models import Area


class Product(models.Model):

    FINISH_CHOICES = [
        ("Glossy", "Glossy"),
        ("Matte", "Matte"),
        ("Satin", "Satin"),
        ("Rustic", "Rustic"),
    ]

    MATERIAL_CHOICES = [
        ("Ceramic", "Ceramic"),
        ("Porcelain", "Porcelain"),
        ("Vitrified", "Vitrified"),
        ("Natural Stone", "Natural Stone"),
    ]

    name = models.CharField(max_length=200)

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
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

    size = models.CharField(max_length=50)

    thickness = models.CharField(max_length=30)

    material = models.CharField(
        max_length=30,
        choices=MATERIAL_CHOICES
    )

    finish = models.CharField(
        max_length=30,
        choices=FINISH_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    thumbnail = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
