from django.db.models import Count
from django.shortcuts import render
from .models import Cart


def dashboard_view(request):
    # 1. Country-wise Users / Carts Count Extract Kara
    country_stats = (
        Cart.objects.values('items__product__country__name', 'items__product__country__code')
        .annotate(total_users=Count('id', distinct=True))
        .order_by('-total_users')
    )

    # Clean data structure
    country_list = []
    for item in country_stats:
        country_name = item['items__product__country__name']
        country_code = item['items__product__country__code']
        if country_name:
            country_list.append({
                'country': country_name,
                'code': country_code.lower() if country_code else 'un',
                'users': item['total_users']
            })

    context = {
        'country_list': country_list,
    }
    return render(request, 'index.html', context)