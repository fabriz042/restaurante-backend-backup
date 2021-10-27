from rest_framework import serializers

from apps.currency.serializers import CurrencySerializer
from apps.operations.models import PaymentType, Purchase, PurchaseDetail
from apps.product.serializers import ProductSerializer
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
            data['provider'] = PaymentTypeSerializer(instance.payment_type).data
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

