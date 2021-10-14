from django.contrib import admin

# Register your models here.
from apps.warehouse.models import Warehouse, WarehouseMovement


class WarehouseMovementTabularInLine(admin.TabularInline):
    model = WarehouseMovement
    extra = 1


class WarehouseAdmin(admin.ModelAdmin):
    inlines = [
        WarehouseMovementTabularInLine
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


class WarehouseMovementAdmin(admin.ModelAdmin):
    inlines = [
        # PrizingTableTabularInline
    ]
    list_display = [
        'id',
        'warehouse',
        'quantity',
        'is_active',
        'restaurant'
    ]
    list_filter = [
        'restaurant',
        'is_active',
        'warehouse',
        'product'
    ]
    search_fields = [
        # 'name'
    ]


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(WarehouseMovement, WarehouseMovementAdmin)
