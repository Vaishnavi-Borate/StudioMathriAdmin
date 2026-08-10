from django.db import models


class Category(models.Model):

    TILE_TYPES = [
        ("Floor", "Floor"),
        ("Wall", "Wall"),
        ("Floor & Wall", "Floor & Wall"),
        ("Special Purpose", "Special Purpose"),
    ]

    name = models.CharField(max_length=150)

    slug = models.SlugField(unique=True)

    icon = models.ImageField(
        upload_to="categories/icons/",
        blank=True,
        null=True
    )

    tile_type = models.CharField(
        max_length=30,
        choices=TILE_TYPES
    )

    description = models.TextField(blank=True)

    display_order = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name