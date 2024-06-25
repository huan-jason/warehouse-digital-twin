from django.contrib import admin
from .. import models


@admin.register(models.UrlCheckNotification)
class UrlCheckNotificationAdmin(admin.ModelAdmin):

    list_display = [
        "url_check",
        "email",
        "remarks",
    ]

    list_filter = [
        "url_check",
    ]

    search_fields = [
        "email",
    ]

    ordering = [
        "url_check",
        "email",
    ]
