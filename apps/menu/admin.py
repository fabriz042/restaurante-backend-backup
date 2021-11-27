from django.contrib import admin

# Register your models here.
from apps.menu.models import MenuCategory, MenuProduct, MenuRecipe


class MenuCategoryTabularInLine(admin.TabularInline):
    model = MenuCategory
    extra = 1


class MenuCategoryAdmin(admin.ModelAdmin):
    inlines = [
        # PurchaseTabularInLine
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


class MenuProductAdmin(admin.ModelAdmin):
    inlines = [
        # PurchaseTabularInLine
    ]
    list_display = [
        'id',
        'category',
        'product',
        'sell_price',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'category',
        'product',
        'is_active'
    ]
    search_fields = [
        # 'name',
    ]


class MenuRecipeAdmin(admin.ModelAdmin):
    inlines = [
        # PurchaseTabularInLine
    ]
    list_display = [
        'id',
        'category',
        'recipe',
        'sell_price',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'category',
        'recipe',
        'is_active'
    ]
    search_fields = [
        # 'name',
    ]


admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuProduct, MenuProductAdmin)
admin.site.register(MenuRecipe, MenuRecipeAdmin)
