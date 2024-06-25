from django.contrib import admin
from .. import models


class UrlCheckInline(admin.TabularInline):
    model = models.UrlCheck
    extra = 0


@admin.register(models.UrlGroup)
class UrlGroupAdmin(admin.ModelAdmin):

    inlines = [
        UrlCheckInline,
    ]