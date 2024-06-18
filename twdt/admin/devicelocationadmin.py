from django.contrib import admin
from twdt import models

@admin.register(models.DeviceLocation)
class DeviceLocationAdmin(admin.ModelAdmin):

    list_display = [
        "device",
        "coordinates",
        "created",
    ]
    search_fields = [
        "device__name",
    ]
    ordering = [
        "device",
        "-created"
    ]