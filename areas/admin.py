from django.contrib import admin
from .models import Area


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "get_state",
        "get_country",
        "pincode",
        "is_active",
    )

    search_fields = (
        "name",
        "city__name",
        "city__state__name",
        "city__state__country__name",
    )

    list_filter = (
        "city__state__country",
        "city__state",
        "city",
        "is_active",
    )

    @admin.display(description="State")
    def get_state(self, obj):
        return obj.city.state.name

    @admin.display(description="Country")
    def get_country(self, obj):
        return obj.city.state.country.name