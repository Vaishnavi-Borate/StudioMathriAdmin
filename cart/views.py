import json
from django.shortcuts import render
from cart.models import CartItem

def admin_index_view(request):
    # Cart Items varun real coordinates fetch kara
    cart_items = CartItem.objects.select_related(
        'cart', 
        'product__country', 
        'product__city', 
        'product__company'
    ).all()

    company_locations = []
    seen = set()

    for item in cart_items:
        prod = item.product
        # Latitude ani Longitude check kara (company level or product level)
        lat = getattr(prod, 'latitude', None) or (prod.company.latitude if prod.company else None)
        lng = getattr(prod, 'longitude', None) or (prod.company.longitude if prod.company else None)
        
        city_name = prod.city.name if prod.city else (prod.company.area.city.name if prod.company and prod.company.area else "Unknown")

        if lat and lng:
            key = f"{lat}_{lng}"
            if key not in seen:
                seen.add(key)
                company_locations.append({
                    'name': f"Cart #{item.cart.id} - {prod.name}",
                    'lat': float(lat),
                    'lng': float(lng),
                    'city': city_name
                })

    # Tumcha Context setup
    context = {
        # Other variables (country_count, product_count, etc.)
        'company_locations': json.dumps(company_locations), # Studio Mathri Map Sathi
    }
    return render(request, 'admin/index.html', context)