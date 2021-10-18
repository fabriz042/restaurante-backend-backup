from django.contrib import admin


# Register your models here.
from apps.operations.models import PaymentType


class PaymentTypeAdmin(admin.ModelAdmin):
    inlines = [
        #    PermissionStackedInLine
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


admin.site.register(PaymentType, PaymentTypeAdmin)
