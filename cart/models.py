from django.db import models
from products.models import Product
# Tumcha City kiwa Area model import kara (e.g., cities.models kiwa locations.models madhun)
from cities.models import City  # Tumchya project nusar path adjust kara


class Cart(models.Model):
    # 📍 LOCATION FIELD ADD KELA AHE
    location = models.ForeignKey(
        City, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Cart Location"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart #{self.id}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def get_product_names(self):
        names = [f"{item.product.name} ({item.quantity})" for item in self.items.all() if item.product]
        return ", ".join(names) if names else "No Items"

    @property
    def get_countries(self):
        countries = set()
        for item in self.items.all():
            if item.product and hasattr(item.product, 'country') and item.product.country:
                countries.add(item.product.country.name)
        return ", ".join(countries) if countries else "Not Specified"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    @property
    def unit_price(self):
        if self.product.discount_price:
            return self.product.discount_price
        return self.product.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity