from django.contrib import admin
from django.utils.html import format_html

from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = (
        "flag_preview",
        "name",
        "code",
        "continent",
        "currency",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = ("name", "code")

    list_filter = ("continent", "is_active")

    ordering = ("name",)

    list_per_page = 10

    save_on_top = True

    date_hierarchy = "created_at"

    def flag_preview(self, obj):
        if obj.flag:
            return format_html(
                '<img src="{}" width="40" height="25" style="border-radius:5px;">',
                obj.flag.url
            )
        return "-"

    flag_preview.short_description = "Flag"