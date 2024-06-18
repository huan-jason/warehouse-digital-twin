from django.contrib import admin
from twdt import models

@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "description",
        "updated",
    ]
    search_fields = [
        "name",
        "description",
    ]
    ordering = [
        "name",
    ]