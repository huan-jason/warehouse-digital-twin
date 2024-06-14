from django.contrib import admin
from twdt import models

@admin.register(models.Rack)
class RackAdmin(admin.ModelAdmin):

    list_display = [
        "warehouse",
        "rack_no",
        "depth",
        "pallet_positions",
        "filled_pallet_positions",
        "occupancy",
    ]
    list_filter = [
        "warehouse",
        "depth",
    ]
    ordering = [
        "warehouse__warehouse_code",
        "rack_no",
    ]