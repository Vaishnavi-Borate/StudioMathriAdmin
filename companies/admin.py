from django.contrib import admin
from django.utils.html import format_html
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "logo_preview",
        "name",
        "country",
        "state",
        "city",
        "area",
        "phone",
        "is_active",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "country__name",
        "state__name",
        "city__name",
        "area__name",
        "phone",
        "email",
    )

    list_filter = (
        "country",
        "state",
        "city",
        "area",
        "is_active",
    )

    ordering = ("name",)

    list_per_page = 15

    save_on_top = True

    readonly_fields = (
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Company Information", {
            "fields": (
                "name",
                "logo",
                "logo_preview",
                "description",
            )
        }),

        ("Location", {
            "fields": (
                "country",
                "state",
                "city",
                "area",
                "address",
            )
        }),

        ("Contact", {
            "fields": (
                "phone",
                "email",
                "website",
                "gst_number",
            )
        }),

        ("Status", {
            "fields": (
                "is_active",
                "created_at",
                "updated_at",
            )
        }),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="70" style="border-radius:8px;">',
                obj.logo.url
            )
        return "No Logo"