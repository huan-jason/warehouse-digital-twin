from django.contrib import admin
from twdt import models

@admin.register(models.RackLocation)
class RackLocationAdmin(admin.ModelAdmin):

    list_display = [
        "rack",
        "location_id",
        "coordinates",
    ]
    list_filter = [
        "rack__warehouse__warehouse_code",
        "rack__rack_no",
    ]
    search_fields = [
        "location_id",
    ]
    ordering = [
        "location_id",
    ]