from rest_framework import serializers
from apps.bill.services import Services
from apps.accounts.serializers import UserSerializer
from apps.client.serializers import ClientSerializer
from apps.currency.serializers import CurrencySerializer
from apps.hall.serializers import TableSerializer
from apps.menu.serializers import MenuItemSerializer
from apps.operations.models import PaymentType, Purchase, PurchaseDetail, Order, OrderDetail, PaymentDocument, Serie, ReturnedOrder
from apps.product.serializers import ProductSerializer
from apps.provider.serializers import ProviderSerializer
from apps.warehouse.models import WarehouseMovement
from apps.warehouse.serializers import WarehouseMovementSerializer, WarehouseSerializer


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'is_active']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id', 'currency', 'sub_total', 'serie', 'correlative',
            'payment_type', 'issue_date', 'igv', 'is_active', 'provider', 'payment_document'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(PurchaseSerializer, self).to_representation(instance)
        if instance.currency:
            data['currency'] = CurrencySerializer(instance.currency).data
        if instance.payment_type:
            data['payment_type'] = PaymentTypeSerializer(instance.payment_type).data
        if instance.provider:
            data['provider'] = ProviderSerializer(instance.provider).data
        if instance.payment_document:
            data['payment_document'] = PaymentDocumentSerializer(instance.payment_document).data
        data['total'] = instance.operation_value
        data['paid'] = instance.paid
        data['debt'] = instance.debt
        data['igv'] = instance.igv_
        return data


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = [
            'id', 'operation', 'subtotal',
            'unitary_value', 'igv', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(PurchaseDetailSerializer, self).to_representation(instance)
        data['product'] = ProductSerializer(instance.movement.product).data
        data['quantity'] = instance.movement.quantity
        data['warehouse'] = WarehouseSerializer(instance.movement.warehouse).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'table',
            'start_datetime',
            'end_datetime',
            'waiter',
            'currency',
            'serie',
            'correlative',
            'payment_type',
            'payment_document',
            'client',
            'igv_percent',
            'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        if instance.table:
            data['table'] = TableSerializer(instance.table).data
        if instance.waiter:
            data['waiter'] = UserSerializer(instance.waiter).data
        if instance.currency:
            data['currency'] = CurrencySerializer(instance.currency).data
        if instance.payment_type:
            data['payment_type'] = PaymentTypeSerializer(instance.payment_type).data
        if instance.payment_document:
            data['payment_document'] = PaymentDocumentSerializer(instance.payment_document).data
        if instance.client:
            data['client'] = ClientSerializer(instance.client).data
        data['total'] = serializers.DecimalField(decimal_places=2, max_digits=8).to_representation(instance.total)
        return data


class OrderSunatSerializer(OrderSerializer):
    def to_representation(self, instance):
        data = super(OrderSunatSerializer, self).to_representation(instance)
        if instance.payment_document:
            if instance.payment_document.electronic_document > 0:
                consult_service = Services(settings=instance.restaurant.billing_settings).consult_bill(instance)
                data['sunat_info'] = consult_service['message'] if 'message' in consult_service else None
                data['sunat_code'] = consult_service['code'] if 'code' in consult_service else None
        try:
            data['bill_order'] = instance.billorder.id
        except Order.billorder.RelatedObjectDoesNotExist:
            data['bill_order'] = None

        has_returned_order = ReturnedOrder.objects.filter(related_order_id=instance.id).first()
        data['has_bill_annulation_order'] = True if has_returned_order else False
        return data


class OrderDetailSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderDetail
        fields = [
            'id',
            'header',
            'menu_item',
            'quantity',
            'state',
            'unit_price',
            'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(OrderDetailSerializer, self).to_representation(instance)
        # if instance.warehouse:
        #    data['warehouse'] = WarehouseSerializer(instance.warehouse).data
        if instance.menu_item:
            data['menu_item'] = MenuItemSerializer(instance.menu_item).data
        return data


class OrderExtendedSerializer(OrderSerializer):
    details = OrderDetailSerializer(many=True, source='details_active')

    class Meta:
        model = Order
        fields = [
            'id',
            'table',
            'start_datetime',
            'end_datetime',
            'waiter',
            'is_active',
            'igv_percent',
            'details'
        ]
        read_only_fields = ('is_active', 'id')


class PaymentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDocument
        fields = [
            'id', 'name', 'is_active', 'electronic_document',
        ]
        read_only_fields = ('is_active', 'id')


class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = [
            'id', 'code', 'correlative', 'payment_document', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(SerieSerializer, self).to_representation(instance)
        if instance.payment_document:
            data['payment_document'] = PaymentDocumentSerializer(instance.payment_document).data
        return data


class ReturnedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnedOrder
        fields = [
            'id',
            'related_order',
            'serie',
            'correlative',
            'payment_document',
            'datetime'
        ]
        read_only_fields = ('is_active', )

    def to_representation(self, instance):
        data = super(ReturnedOrderSerializer, self).to_representation(instance)
        data['related_order_data'] = OrderExtendedSerializer(instance.related_order).data
        if instance.payment_document:
            data['payment_document_data'] = PaymentDocumentSerializer(instance.payment_document).data
        return data


class ReturnedOrderSunatSerializer(ReturnedOrderSerializer):
    def to_representation(self, instance):
        data = super(ReturnedOrderSunatSerializer, self).to_representation(instance)
        if instance.payment_document:
            if instance.payment_document.electronic_document > 0:
                consult_service = Services(settings=instance.restaurant.billing_settings).consult_bill(instance)
                data['sunat_info'] = consult_service['message'] if 'message' in consult_service else None
                data['sunat_code'] = consult_service['code'] if 'code' in consult_service else None
        try:
            data['bill_returned_order'] = instance.billreturnedorder.id
        except Order.billorder.RelatedObjectDoesNotExist:
            data['bill_returned_order'] = None
        return data
