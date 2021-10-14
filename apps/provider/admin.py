from django.contrib import admin

# Register your models here.
from apps.document_type.models import DocumentType
from apps.provider.models import Provider, PrizingTable


class PrizingTableTabularInline(admin.TabularInline):
    model = PrizingTable
    extra = 1


class ProviderAdmin(admin.ModelAdmin):
    inlines = [
        PrizingTableTabularInline
    ]
    list_display = [
        'id',
        'name',
        'document_type',
        'document',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active',
        'document_type'
    ]
    search_fields = [
        'name',
    ]


class PrizingTableAdmin(admin.ModelAdmin):
    inlines = [
        # DocumentTypeStackedInLine
    ]
    list_display = [
        'id',
        'provider',
        'product',
        'currency',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'provider',
        'product',
        'currency',
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'provider',
        'product',
        'currency',
        'restaurant',
        'is_active'
    ]


admin.site.register(Provider, ProviderAdmin)
admin.site.register(PrizingTable, PrizingTableAdmin)
