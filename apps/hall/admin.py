from django.contrib import admin

# Register your models here.
from apps.hall.models import Hall, Table


class TableTabularInLine(admin.TabularInline):
    model = Table
    extra = 1


class TableAdmin(admin.ModelAdmin):
    inlines = [
        # PurchaseTabularInLine
    ]
    list_display = [
        'id',
        'name',
        'hall',
        'capacity',
        'is_active'
    ]
    list_filter = [
        'hall',
        'capacity',
        'is_active'
    ]
    search_fields = [
        'name',
    ]


class HallTabularInLine(admin.TabularInline):
    model = Hall
    extra = 0


class HallAdmin(admin.ModelAdmin):
    inlines = [
        TableTabularInLine
    ]
    list_display = [
        'id',
        'name',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'name',
    ]


admin.site.register(Hall, HallAdmin)
admin.site.register(Table, TableAdmin)
