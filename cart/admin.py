from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

    fields = (
        "product",
        "quantity",
        "unit_price",
        "total_price",
    )

    readonly_fields = (
        "unit_price",
        "total_price",
    )

    # autocomplete_fields REMOVED


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "display_products",
        "location",
        "display_countries",
        "display_total_items",
        "display_total_price",
        "created_at",
    )

    readonly_fields = (
        "total_items",
        "total_price",
        "display_countries",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Cart Location & Info",
            {
                "fields": (
                    "location",
                ),
            },
        ),
        (
            "Cart Summary",
            {
                "fields": (
                    "total_items",
                    "total_price",
                    "display_countries",
                ),
            },
        ),
        (
            "Cart Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    inlines = [
        CartItemInline,
    ]

    @admin.display(description="Cart Products")
    def display_products(self, obj):
        names = obj.get_product_names

        if names != "No Items":
            return f"📦 {names}"

        return "Empty Cart"

    @admin.display(description="Product Location")
    def display_countries(self, obj):
        countries = obj.get_countries

        if countries != "Not Specified":
            return f"🌍 {countries}"

        return "N/A"

    @admin.display(description="Total Items")
    def display_total_items(self, obj):
        return obj.total_items

    @admin.display(description="Total Price")
    def display_total_price(self, obj):
        return f"₹ {obj.total_price:,.2f}"