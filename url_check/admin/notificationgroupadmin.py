from django.contrib import admin
from .. import models


class NotificationInline(admin.TabularInline):
    model = models.Notification
    extra = 0


@admin.register(models.NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):

    inlines = [
        NotificationInline,
    ]