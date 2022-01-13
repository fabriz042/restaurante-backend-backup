from django.contrib import admin

# Register your models here.
from apps.client.models import Client


class ClientAdmin(admin.ModelAdmin):
    inlines = [
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


admin.site.register(Client, ClientAdmin)
