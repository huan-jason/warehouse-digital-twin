from django.contrib import admin
from twdt import models

@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):

    list_display = [
        "warehouse_code",
        "name",
        "address",
        "remarks",
    ]
    search_fields = [
        "warehouse_code",
        "name",
        "address",
        "remarks",
    ]
    ordering = [
        "warehouse_code",
    ]