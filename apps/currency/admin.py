from django.contrib import admin

from apps.currency.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    inlines = [
        #    PermissionStackedInLine
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
