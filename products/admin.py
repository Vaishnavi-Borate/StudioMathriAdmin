from django.contrib import admin, messages
from django.db.models import Q
from django.utils.html import format_html

from .models import Product
from cart.models import Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "thumbnail_preview",
        "name",
        "sku",
        "company",
        "category",
        "price",
        "stock",
        "is_featured",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = (
        'name',
        'sku',
        'category__name',
        'company__name',
        'country__name',
        'state__name',
        'city__name',
        'area__name',
    )

    list_filter = (
        "company",
        "category",
        "material",
        "finish",
        "is_featured",
        "is_active",
    )

    # 1. Foreign Key Performance & JOIN Fix (Company & Category search sathi essential)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('company', 'category', 'country', 'state', 'city', 'area')

    # 2. Perfect Multi-Model Search Logic
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Clean and split search terms for full matching
            search_words = search_term.split()
            for word in search_words:
                queryset = queryset.filter(
                    Q(name__icontains=word) |
                    Q(sku__icontains=word) |
                    Q(category__name__icontains=word) |
                    Q(company__name__icontains=word) |
                    Q(country__name__icontains=word) |
                    Q(state__name__icontains=word) |
                    Q(city__name__icontains=word) |
                    Q(area__name__icontains=word)
                )
            use_distinct = True

        return queryset, use_distinct

    ordering = ("name",)

    list_per_page = 20

    save_on_top = True

    readonly_fields = (
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )

    actions = [
        "add_selected_to_cart",
    ]

    fieldsets = (

        ("Basic Information", {
            "fields": (
                "name",
                "sku",
                "thumbnail",
                "thumbnail_preview",
                "description",
            )
        }),

        ("Classification", {
            "fields": (
                "company",
                "category",
            )
        }),

        ("Location", {
            "fields": (
                "country",
                "state",
                "city",
                "area",
            )
        }),

        ("Specifications", {
            "fields": (
                "size",
                "thickness",
                "material",
                "finish",
            )
        }),

        ("Pricing", {
            "fields": (
                "price",
                "discount_price",
                "stock",
            )
        }),

        ("Status", {
            "fields": (
                "is_featured",
                "is_active",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Image")
    def thumbnail_preview(self, obj):

        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="border-radius:8px; object-fit:cover;">',
                obj.thumbnail.url
            )

        return "No Image"

    @admin.action(description="🛒 Add selected products to Cart")
    def add_selected_to_cart(self, request, queryset):

        # Get existing cart or create a new one
        cart = Cart.objects.first()

        if not cart:
            cart = Cart.objects.create()

        added_count = 0
        updated_count = 0

        for product in queryset:

            # Don't add inactive or out-of-stock products
            if not product.is_active:
                continue

            if product.stock <= 0:
                continue

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    "quantity": 1
                }
            )

            if created:
                added_count += 1
            else:
                cart_item.quantity += 1

                # Don't exceed available stock
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock

                cart_item.save()

                updated_count += 1

        if added_count or updated_count:

            message = (
                f"{added_count} product(s) added to cart."
            )

            if updated_count:
                message += (
                    f" {updated_count} existing product(s) "
                    f"quantity updated."
                )

            self.message_user(
                request,
                message,
                messages.SUCCESS
            )

        else:

            self.message_user(
                request,
                "No active/in-stock products were added.",
                messages.WARNING
            )