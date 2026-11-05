from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_name",
        "contact_name",
        "email",
        "phone",
        "is_active",
    )
    search_fields = ("company_name", "contact_name", "email")
    list_filter = ("is_active",)