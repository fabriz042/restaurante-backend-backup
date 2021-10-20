from django.contrib import admin

# Register your models here.
from apps.accounts.admin import PurchaseTabularInLine
from apps.operations.models import PaymentType, Purchase, PurchaseDetail


class PurchaseDetailTabularInLine(admin.TabularInline):
    model = PurchaseDetail
    extra = 1


class PaymentTypeAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseTabularInLine
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


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseDetailTabularInLine
    ]
    list_display = [
        'id',
        'provider',
        'serie',
        'correlative',
        'is_active',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        # 'name',
    ]


admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
