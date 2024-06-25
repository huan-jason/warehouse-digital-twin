from django.contrib import admin
from .. import models


class UrlCheckNotificationInline(admin.TabularInline):
    model = models.UrlCheckNotification
    extra = 0


@admin.register(models.UrlCheck)
class UrlCheckAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "url_group",
        "url",
        "notification_group",
        "remarks",
        "status_code",
        "check_text",
    ]

    list_filter = [
        "url_group",
        "notification_group",
        "status_code",
    ]

    search_fields = [
        "name",
        "url",
        "remarks",
        "check_text",
    ]

    ordering = [
        "url_group__name",
        "name",
    ]

    inlines = [
        UrlCheckNotificationInline,
    ]
