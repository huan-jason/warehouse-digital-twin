from django.contrib import admin
from .. import models


@admin.register(models.UrlCheckFailure)
class UrlCheckFailureAdmin(admin.ModelAdmin):

    list_display = [
        "url_check",
        "time",
        "remarks",
        "status_code",
    ]

    list_filter = [
        "url_check",
        "time",
        "status_code",
    ]

    search_fields = [
        "url_check__url",
        "remarks",
    ]

    ordering = [
        "-time",
    ]
