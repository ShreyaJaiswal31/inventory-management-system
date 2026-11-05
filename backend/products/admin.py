from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "sku",
        "category",
        "supplier",
        "price",
        "quantity",
        "reorder_level",
        "is_active",
        "created_at",
    )


    list_display_links = ("name",)
    search_fields = ("name", "sku")
    list_filter = ("is_active", "category", "supplier")