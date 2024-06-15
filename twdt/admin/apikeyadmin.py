from django.contrib import admin
from twdt import models

@admin.register(models.ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):

    list_display = [
        "api_key",
        "expiry",
        "remarks",
        "ip_addresses",
        "created",
        "updated",
    ]
    search_fields = [
        "api_key",
        "remarks",
        "ip_addresses",
    ]
    ordering = [
        "-updated",
    ]