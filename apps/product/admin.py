from django.contrib import admin

# Register your models here.
from apps.product.models import Brand, ProductCategory


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


admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
