from django.contrib import admin
from .. import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = [
        "email",
        "notification_group",
        "remarks",
    ]
