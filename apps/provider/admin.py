from django.contrib import admin

# Register your models here.
from apps.document_type.models import DocumentType
from apps.provider.models import Provider


class ProviderAdmin(admin.ModelAdmin):
    inlines = [
        # DocumentTypeStackedInLine
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


admin.site.register(Provider, ProviderAdmin)
