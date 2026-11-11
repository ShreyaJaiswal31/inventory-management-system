from django.contrib import admin
from .models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "movement_type",
        "quantity",
        "created_at",
    )

    search_fields = ("product__name", "product__sku")
    list_filter = ("movement_type", "created_at")
    readonly_fields = ("created_at",)


def has_add_permission(self, request):
    return False

def has_change_permission(self, request, obj=None):
    return False

def has_delete_permission(self, request, obj=None):
    return False