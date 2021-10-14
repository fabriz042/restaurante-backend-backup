from django.contrib import admin

from apps.currency.models import Currency
from apps.provider.models import PrizingTable


class PrizingTableTabularInline(admin.TabularInline):
    model = PrizingTable
    extra = 1


class CurrencyAdmin(admin.ModelAdmin):
    inlines = [
        PrizingTableTabularInline
    ]
    list_display = [
        'id',
        'name',
        'symbol',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'name',
        'symbol'
    ]


admin.site.register(Currency, CurrencyAdmin)
