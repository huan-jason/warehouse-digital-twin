from django.contrib import admin
from twdt import models

@admin.register(models.Pallet)
class PalletAdmin(admin.ModelAdmin):

    list_display = [
        "rack_location",
        "pallet_id",
        "owner",
        "product_code",
        "description",
        "expiry_date",
        "quantity_on_hand",
        "age",
        "balance_shelve_life_to_expire",
        "balance_shelf_life_percentage",
        "product_group",
    ]
    list_filter = [
        "rack_location__rack__warehouse__warehouse_code",
        "owner",
        "product_group",
    ]
    search_fields = [
        "pallet_id",
        "owner",
        "product_code",
        "description",
        "product_group",
    ]
    ordering = [
        "pallet_id",
    ]