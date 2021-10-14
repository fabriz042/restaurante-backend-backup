from django.contrib import admin

# Register your models here.
from apps.product.models import Brand, ProductCategory, MeasurementUnit, Product
from apps.provider.models import PrizingTable


class PrizingTableTabularInline(admin.TabularInline):
    model = PrizingTable
    extra = 1


class BrandAdmin(admin.ModelAdmin):
    inlines = [
        # DocumentTypeStackedInLine
    ]
    list_display = [
        'id',
        'name',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'name',
    ]


class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [
        # DocumentTypeStackedInLine
    ]
    list_display = [
        'id',
        'name',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'name',
    ]


class MeasurementUnitAdmin(admin.ModelAdmin):
    inlines = [
        # DocumentTypeStackedInLine
    ]
    list_display = [
        'id',
        'name',
        'code',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'name',
        'code'
    ]


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        PrizingTableTabularInline
    ]
    list_display = [
        'id',
        'name',
        'category',
        'is_active',
        'restaurant'
    ]
    list_filter = [
        'restaurant',
        'category',
        'is_active'
    ]
    search_fields = [
        'name'
    ]


admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(Product, ProductAdmin)
