from django.contrib.admin import AdminSite

class StudioMathriAdminSite(AdminSite):
    site_header = "Studio Mathri Admin"
    site_title = "Studio Mathri"
    index_title = "Dashboard"

    def each_context(self, request):
        context = super().each_context(request)

        from countries.models import Country
        from states.models import State
        from cities.models import City
        from areas.models import Area
        from companies.models import Company
        from categories.models import Category
        from products.models import Product
        from django.contrib.auth.models import User

        context["country_count"] = Country.objects.count()
        context["state_count"] = State.objects.count()
        context["city_count"] = City.objects.count()
        context["area_count"] = Area.objects.count()

        context["company_count"] = Company.objects.count()
        context["category_count"] = Category.objects.count()
        context["product_count"] = Product.objects.count()

        context["user_count"] = User.objects.count()

        return context


admin_site = StudioMathriAdminSite(name="studio_admin")