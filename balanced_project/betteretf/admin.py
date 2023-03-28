from django.contrib import admin
from .models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory

# Register your models here.


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'type', 'category', 'beta', 'exp_ratio')


@admin.register(HoldingsBreakdown)
class HoldingsAdmin(admin.ModelAdmin):
    list_display = ('ticker',)


@admin.register(SectorsBreakdown)
class SectorsAdmin(admin.ModelAdmin):
    list_display = ('ticker',)


@admin.register(ThreeYearHistory)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'date')
