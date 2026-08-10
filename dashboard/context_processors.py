import json

from django.contrib.auth.models import User
from django.db.models import Count

from countries.models import Country
from states.models import State
from cities.models import City
from areas.models import Area
from companies.models import Company
from categories.models import Category
from products.models import Product
from cart.models import Cart

def dashboard_stats(request):

    # -------- Product by Category --------
    category_data = (
        Product.objects.values("category__name")
        .annotate(total=Count("id"))
        .order_by("category__name")
    )

    category_labels = [item["category__name"] for item in category_data]
    category_counts = [item["total"] for item in category_data]

    # -------- Product by Company --------
    company_data = (
        Product.objects.values("company__name")
        .annotate(total=Count("id"))
        .order_by("company__name")
    )

    company_labels = [item["company__name"] for item in company_data]
    company_counts = [item["total"] for item in company_data]

    return {

        # Total Counts
        "country_count": Country.objects.count(),
        "state_count": State.objects.count(),
        "city_count": City.objects.count(),
        "area_count": Area.objects.count(),

        "company_count": Company.objects.count(),
        "category_count": Category.objects.count(),
        "product_count": Product.objects.count(),

        "user_count": User.objects.count(),

        # Active Counts
        "active_countries": Country.objects.filter(is_active=True).count(),
        "active_states": State.objects.filter(is_active=True).count(),
        "active_cities": City.objects.filter(is_active=True).count(),
        "active_areas": Area.objects.filter(is_active=True).count(),

        "active_companies": Company.objects.filter(is_active=True).count(),
        "active_categories": Category.objects.filter(is_active=True).count(),
        "active_products": Product.objects.filter(is_active=True).count(),

        # Charts
        "category_labels": json.dumps(category_labels),
        "category_counts": json.dumps(category_counts),

        "company_labels": json.dumps(company_labels),
        "company_counts": json.dumps(company_counts),

        # Recent Products
        "recent_products": Product.objects.select_related(
            "category",
            "company"
        ).order_by("-id")[:5],
    }
from cart.models import Cart


def cart_context(request):
    cart_count = 0
    cart_items = 0
    cart_total = 0

    if request.user.is_authenticated:
        carts = Cart.objects.all()

        cart_count = carts.count()
        cart_items = sum(cart.total_items for cart in carts)
        cart_total = sum(cart.total_price for cart in carts)

    return {
        "cart_count": cart_count,
        "cart_items": cart_items,
        "cart_total": cart_total,
    }