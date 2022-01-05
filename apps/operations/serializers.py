from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.currency.serializers import CurrencySerializer
from apps.hall.serializers import TableSerializer
from apps.menu.serializers import MenuItemSerializer
from apps.operations.models import PaymentType, Purchase, PurchaseDetail, Order, OrderDetail
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
            'payment_type', 'issue_date', 'igv', 'is_active', 'provider'
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
        data['total'] = instance.operation_value
        data['paid'] = instance.paid
        data['debt'] = instance.debt
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
            'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        if instance.table:
            data['table'] = TableSerializer(instance.table).data
        if instance.waiter:
            data['waiter'] = UserSerializer(instance.waiter).data
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
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'table',
            'start_datetime',
            'end_datetime',
            'waiter',
            'is_active',
            'details'
        ]
        read_only_fields = ('is_active', 'id')
