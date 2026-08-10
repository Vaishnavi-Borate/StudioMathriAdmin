from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "icon_preview",
        "name",
        "tile_type",
        "is_featured",
        "display_order",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "tile_type",
        "is_featured",
        "is_active",
    )

    ordering = (
        "display_order",
        "name",
    )

    list_per_page = 15

    save_on_top = True

    readonly_fields = (
        "icon_preview",
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (

        ("Category Information", {
            "fields": (
                "name",
                "slug",
                "tile_type",
                "description",
            )
        }),

        ("Appearance", {
            "fields": (
                "icon",
                "icon_preview",
            )
        }),

        ("Settings", {
            "fields": (
                "display_order",
                "is_featured",
                "is_active",
            )
        }),

        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Icon")
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;">',
                obj.icon.url
            )
        return "No Icon"
