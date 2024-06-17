from django.contrib import admin

from twdt import models
from .palletadmin import PalletAdmin


@admin.register(models.PalletHistory)
class PalletHistoryAdmin(PalletAdmin):
    pass
