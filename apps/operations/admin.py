from django.contrib import admin

# Register your models here.
from apps.accounts.admin import PurchaseTabularInLine
from apps.operations.models import PaymentType, Purchase, PurchaseDetail, Order, PaymentDocument, Serie, OrderDetail, ReturnedOrder
from apps.payments.models import Payment


class PaymentTabularInLine(admin.TabularInline):
    model = Payment
    extra = 1


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


class PaymentDocumentAdmin(admin.ModelAdmin):
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


class SerieAdmin(admin.ModelAdmin):
    inlines = [
        # PurchaseTabularInLine
    ]
    list_display = [
        'id',
        'code',
        'restaurant',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'is_active'
    ]
    search_fields = [
        'code',
    ]


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseDetailTabularInLine,
        PaymentTabularInLine
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


class OrderDetailTabularInLine(admin.TabularInline):
    model = OrderDetail
    extra = 0
    fields = [
        'menu_item',
        'quantity',
        'state',
        'unit_price'
    ]


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderDetailTabularInLine
    ]
    list_display = [
        'id',
        'restaurant',
        'table',
        'serie',
        'correlative',
        'total',
        'start_datetime',
        'end_datetime',
        'waiter',
        'is_active'
    ]
    list_filter = [
        'restaurant',
        'table',
        'waiter',
        'is_active'
    ]
    search_fields = [
        # 'name',
    ]


class ReturnedOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'restaurant',
        'related_order',
        'serie',
        'correlative',
        'total',
        'datetime',
        'is_active',
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
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentDocument, PaymentDocumentAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(OrderDetail)
admin.site.register(ReturnedOrder, ReturnedOrderAdmin)
