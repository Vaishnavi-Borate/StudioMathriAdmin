from django.contrib import admin
from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "state",
        "get_country",
        "pincode",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "state__name",
        "state__country__name",
    )

    list_filter = (
        "state__country",
        "state",
        "is_active",
    )

    ordering = ("state", "name")

    list_per_page = 10

    save_on_top = True

    date_hierarchy = "created_at"

    @admin.display(description="Country")
    def get_country(self, obj):
        return obj.state.country.name
