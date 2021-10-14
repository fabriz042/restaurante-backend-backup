from django.contrib import admin


# Register your models here.
from apps.warehouse.models import Warehouse


class WarehouseAdmin(admin.ModelAdmin):
    inlines = [
        # PrizingTableTabularInline
    ]
    list_display = [
        'id',
        'name',
        'is_main',
        'is_active',
        'restaurant'
    ]
    list_filter = [
        'restaurant',
        'is_main',
        'is_active'
    ]
    search_fields = [
        'name'
    ]


admin.site.register(Warehouse, WarehouseAdmin)
