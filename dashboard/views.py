from django.db.models.aggregates import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from countries.models import Country
from states.models import State
from cities.models import City
from areas.models import Area
from companies.models import Company
from categories.models import Category
from products.models import Product
from cart.models import Cart

from django.contrib.auth.models import User


@login_required
def dashboard(request):

    context = {

        # =========================
        # COUNTS
        # =========================

        "country_count": Country.objects.count(),
        "state_count": State.objects.count(),
        "city_count": City.objects.count(),
        "area_count": Area.objects.count(),
        "company_count": Company.objects.count(),
        "category_count": Category.objects.count(),
        "product_count": Product.objects.count(),
        "user_count": User.objects.count(),

        # =========================
        # ACTIVE COUNTS
        # =========================

        "active_countries": Country.objects.filter(is_active=True).count(),
        "active_states": State.objects.filter(is_active=True).count(),
        "active_cities": City.objects.filter(is_active=True).count(),
        "active_areas": Area.objects.filter(is_active=True).count(),
        "active_companies": Company.objects.filter(is_active=True).count(),
        "active_categories": Category.objects.filter(is_active=True).count(),
        "active_products": Product.objects.filter(is_active=True).count(),

        # =========================
        # CART
        # =========================

        "cart_count": Cart.objects.count(),

        "cart_total_items": sum(
            cart.total_items for cart in Cart.objects.all()
        ),

        "cart_total_price": sum(
            cart.total_price for cart in Cart.objects.all()
        ),
    }
def dashboard_view(request):
    # Country-wise Users / Carts Count Fetch Kara
    country_stats = (
        Cart.objects.values('items__product__country__name')
        .annotate(total_users=Count('id', distinct=True))
        .order_by('-total_users')
    )

    country_list = []
    for item in country_stats:
        country_name = item['items__product__country__name']
        if country_name:
            country_list.append({
                'country': country_name,
                'users': item['total_users']
            })

    # Fallback Data: Jar Database madhe direct relation nasel tar Product/Company Country check kara
    if not country_list:
        # Fetch directly from Cart items
        carts = Cart.objects.prefetch_related('items__product__country').all()
        country_count_map = {}

        for cart in carts:
            for item in cart.items.all():
                if item.product and hasattr(item.product, 'country') and item.product.country:
                    c_name = item.product.country.name
                    country_count_map[c_name] = country_count_map.get(c_name, 0) + 1

        for c_name, count in country_count_map.items():
            country_list.append({'country': c_name, 'users': count})

    # Context Pass Kara
    context = {
        'country_list': country_list,
        # Tumche baki context variables hithe rahtil (e.g., country_count, product_count)
    }

    return render(request, 'index.html', context)
