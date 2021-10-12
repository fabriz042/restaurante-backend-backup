from django.contrib import admin

# Register your models here.
from apps.product.models import Brand, ProductCategory, MeasurementUnit


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


admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
