from django.contrib import admin
from .models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "capital",
        "code",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "country__name",
        "capital",
    )

    list_filter = (
        "country",
        "is_active",
    )

    ordering = ("country", "name")

    list_per_page = 10

    save_on_top = True

    date_hierarchy = "created_at"