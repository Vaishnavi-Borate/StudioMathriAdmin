import json
from datetime import timedelta

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth.models import User

from countries.models import Country
from states.models import State
from cities.models import City
from areas.models import Area
from companies.models import Company
from categories.models import Category
from products.models import Product
from cart.models import Cart
from django.db.models import Count
    

def analytics_dashboard(request):

    # =========================================
    # 0. COUNTRY ISO CODE HELPER
    # =========================================

    country_codes = {
        "India": "IN",
        "United States": "US",
        "United Kingdom": "GB",
        "Canada": "CA",
        "Australia": "AU",
        "Germany": "DE",
        "France": "FR",
        "Italy": "IT",
        "Spain": "ES",
        "Brazil": "BR",
        "China": "CN",
        "Japan": "JP",
        "South Korea": "KR",
        "Singapore": "SG",
        "United Arab Emirates": "AE",
        "Saudi Arabia": "SA",
        "Russia": "RU",
        "South Africa": "ZA",
        "Mexico": "MX",
        "Nepal": "NP",
        "Bangladesh": "BD",
        "Sri Lanka": "LK",
    }

    # =========================================
    # ENSURE DEMO COUNTRIES IF EMPTY
    # =========================================

    if not Country.objects.exists():

        Country.objects.create(
            name="India",
            code="IN"
        )

        Country.objects.create(
            name="United States",
            code="US"
        )

    # =========================================
    # 1. TOP SUMMARY CARDS COUNTS
    # =========================================

    country_count = Country.objects.count()
    state_count = State.objects.count()
    city_count = City.objects.count()
    area_count = Area.objects.count()

    company_count = Company.objects.count()
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    user_count = User.objects.count()
    cart_count = Cart.objects.count()

    # =========================================
    # 2. BAR CHART: PRODUCTS BY CATEGORY
    # =========================================

    category_data = (
        Product.objects
        .values("category__name")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    category_labels = [
        item["category__name"] or "General"
        for item in category_data
    ]

    category_counts = [
        item["total"]
        for item in category_data
    ]

    # =========================================
    # 3. PIE CHART: PRODUCTS BY COMPANY
    # =========================================

    company_data = (
        Product.objects
        .values("company__name")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")[:5]
    )

    company_labels = [
        item["company__name"] or "Standard"
        for item in company_data
    ]

    company_counts = [
        item["total"]
        for item in company_data
    ]

    # =========================================
    # 4. COUNTRY DATA FROM PRODUCTS
    # =========================================
   # 4. COUNTRY DATA DIRECT FETCH FROM PRODUCTS & CARTS
    country_list = []
    map_country_data = {}

    # Products kinva Cart madhun countries fetch karne
    product_countries = Product.objects.exclude(company__area__city__state__country__isnull=True).values(
        'company__area__city__state__country__name', 
        'company__area__city__state__country__code'
    ).annotate(total=Count('id'))

    for item in product_countries:
        c_name = item.get('company__area__city__state__country__name')
        c_code = item.get('company__area__city__state__country__code')
        total = item.get('total', 0)

        if c_name:
            country_list.append({
                "country": c_name,
                "users": total
            })
            if c_code:
                map_country_data[c_code] = total

    # Jar ekhadi pan country database madhun ali nahi, tar default values taku jyamule list ani map disel
    if not country_list:
        country_list = [
            {"country": "India", "users": 35},
            {"country": "Spain", "users": 20}
        ]
        map_country_data = {"IN": 35, "ES": 20}
    # =========================================

    product_country_data = (
        Product.objects
        .filter(
            country__isnull=False
        )
        .values(
            "country_id",
            "country__name",
            "country__code"
        )
        .annotate(
            products=Count("id")
        )
        .order_by("-products")
    )

    # Convert product country data into dictionary
    # Example:
    #
    # {
    #     1: {
    #         "products": 5,
    #         "name": "India",
    #         "code": "IN"
    #     }
    # }

    product_country_map = {}

    for item in product_country_data:

        country_id = item["country_id"]

        country_name = item["country__name"]

        country_code = item["country__code"]

        if not country_code and country_name:
            country_code = country_codes.get(
                country_name,
                ""
            )

        product_country_map[country_id] = {
            "products": item["products"],
            "name": country_name,
            "code": country_code.upper()
            if country_code
            else ""
        }

    # =========================================
    # COUNTRY LIST
    # =========================================
    #
    # IMPORTANT:
    # All countries from Country table are shown.
    #
    # Even if a country has 0 products,
    # it will still appear in the dashboard.
    #
    # =========================================

    country_list = []
    map_country_data = {}

    db_countries = Country.objects.all().order_by("name")

    for country in db_countries:

        country_name = country.name

        country_code = getattr(
            country,
            "code",
            ""
        )

        if not country_code and country_name:

            country_code = country_codes.get(
                country_name,
                ""
            )

        country_code = (
            country_code.upper()
            if country_code
            else ""
        )

        # Product count for this country
        product_info = product_country_map.get(
            country.id,
            {}
        )

        product_total = product_info.get(
            "products",
            0
        )

        # =====================================
        # ADD COUNTRY TO LEFT SIDE LIST
        # =====================================

        country_list.append({

            "country": country_name,

            # New correct value
            "products": product_total,

            # Kept for old template compatibility
            "users": product_total,

            "code": country_code,
        })

        # =====================================
        # ADD COUNTRY TO WORLD MAP
        # =====================================

        if country_code:

            map_country_data[country_code] = (
                product_total
            )

    # =========================================
    # 5. RECENT PRODUCTS TABLE
    # =========================================

    recent_products = (
        Product.objects
        .select_related(
            "category",
            "company"
        )
        .order_by("-id")[:5]
    )

    # =========================================
    # 6. DYNAMIC MONTHLY STATISTICS
    # =========================================

    today = timezone.now()

    months = []

    current_year = today.year
    current_month = today.month

    for i in range(5, -1, -1):

        month = current_month - i
        year = current_year

        while month <= 0:

            month += 12
            year -= 1

        months.append(
            (year, month)
        )

    last_6_months = [
        timezone.datetime(
            year,
            month,
            1
        ).strftime("%b")
        for year, month in months
    ]

    # =========================================
    # MONTHLY COUNT FUNCTION
    # =========================================

    def get_monthly_counts(
        model,
        date_field
    ):

        monthly_qs = (
            model.objects
            .annotate(
                month=TruncMonth(
                    date_field
                )
            )
            .values("month")
            .annotate(
                total=Count("id")
            )
            .order_by("month")
        )

        month_map = {}

        for entry in monthly_qs:

            if entry["month"]:

                key = (
                    entry["month"].year,
                    entry["month"].month
                )

                month_map[key] = (
                    entry["total"]
                )

        return [
            month_map.get(
                (year, month),
                0
            )
            for year, month in months
        ]

    # =========================================
    # ACTUAL MONTHLY DATA
    # =========================================

    products_monthly = get_monthly_counts(
        Product,
        "created_at"
    )

    companies_monthly = get_monthly_counts(
        Company,
        "created_at"
    )

    users_monthly = get_monthly_counts(
        User,
        "date_joined"
    )

    carts_monthly = get_monthly_counts(
        Cart,
        "created_at"
    )

    # =========================================
    # OVERALL ACTIVITY
    # =========================================

    overview_monthly = [
        p + c + u + cart
        for p, c, u, cart in zip(
            products_monthly,
            companies_monthly,
            users_monthly,
            carts_monthly
        )
    ]

    # =========================================
    # STATISTICS DATA
    # =========================================

    stats_data = {

        "overview": {

            "labels": last_6_months,

            "data": overview_monthly,

            "label": "Overall Activity",
        },

        "products": {

            "labels": last_6_months,

            "data": products_monthly,

            "label": "Products Added",
        },

        "carts": {

            "labels": last_6_months,

            "data": carts_monthly,

            "label": "Carts Created",
        },

        "customers": {

            "labels": last_6_months,

            "data": users_monthly,

            "label": "New Registered Users",
        },
    }

    # =========================================
    # 7. FINAL CONTEXT
    # =========================================

    context = {

        # =====================================
        # Main counts
        # =====================================

        "countries": country_count,

        "states": state_count,

        "cities": city_count,

        "areas": area_count,

        "companies": company_count,

        "categories": category_count,

        "products": product_count,

        "users": user_count,

        "carts": cart_count,

        # =====================================
        # Individual card counts
        # =====================================

        "country_count": country_count,

        "state_count": state_count,

        "city_count": city_count,

        "area_count": area_count,

        "company_count": company_count,

        "category_count": category_count,

        "product_count": product_count,

        "user_count": user_count,

        "cart_count": cart_count,

        # =====================================
        # Category chart
        # =====================================

        "category_labels": json.dumps(
            category_labels
        ),

        "category_counts": json.dumps(
            category_counts
        ),

        # =====================================
        # Company pie chart
        # =====================================

        "company_labels": json.dumps(
            company_labels
        ),

        "company_counts": json.dumps(
            company_counts
        ),

        # =====================================
        # Country list
        # =====================================

        "country_list": [
            {
                "country": country_name,
                "products": item["products"],
            }
            for country_name, item in country_data.items()
        ],

        # =====================================
        # World map data
        # =====================================

        "map_country_data_json": json.dumps(
            map_country_data
        ),

        # =====================================
        # Recent products
        # =====================================

        "recent_products": recent_products,

        # =====================================
        # Statistics graph
        # =====================================

        "stats_data_json": json.dumps(
            stats_data
        ),
    }

    # =========================================
    # RENDER DASHBOARD
    # =========================================

    return render(
        request,
        "admin/index.html",
        context
    )