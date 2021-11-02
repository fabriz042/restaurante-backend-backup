from django.contrib import admin

# Register your models here.
from apps.recipe.models import Recipe, RecipeDetail


class RecipeDetailTabularInLine(admin.TabularInline):
    model = RecipeDetail
    extra = 1
    fields = [
        'quantity',
        'product',
        'is_active'
    ]


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeDetailTabularInLine
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
        'name'
    ]


admin.site.register(Recipe, RecipeAdmin)
