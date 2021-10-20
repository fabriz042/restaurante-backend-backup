from rest_framework import serializers

from apps.currency.serializers import CurrencySerializer
from apps.operations.models import PaymentType, Purchase


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'is_active']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id', 'currency', 'sub_total', 'serie', 'correlative',
            'payment_type', 'issue_date', 'igv', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(PurchaseSerializer, self).to_representation(instance)
        if instance.currency:
            data['currency'] = CurrencySerializer(instance.currency).data
        if instance.payment_type:
            data['payment_type'] = PaymentTypeSerializer(instance.payment_type).data
        return data
