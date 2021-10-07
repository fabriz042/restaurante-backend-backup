from django.contrib import admin


# Register your models here.
from apps.document_type.models import DocumentType


class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = [
        #    PermissionStackedInLine
    ]
    list_display = [
        'id',
        'name',
        'code',
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


admin.site.register(DocumentType, DocumentTypeAdmin)
