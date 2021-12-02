from rest_framework import serializers

from apps.currency.serializers import CurrencySerializer
from apps.document_type.serializers import DocumentTypeSerializer
from apps.product.serializers import ProductSerializer, ProductMiniSerializer
from apps.provider.models import Provider, PrizingTable


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'document_type',
            'document',
            'phone',
            'address',
            'is_active'
        ]
        extra_kwargs = {
            'document_type': {'required': False},
            'document': {'required': False},
            'phone': {'required': False},
            'address': {'required': False}
        }

    def to_representation(self, instance):
        data = super(ProviderSerializer, self).to_representation(instance)
        if instance.document_type:
            data['document_type'] = DocumentTypeSerializer(instance=instance.document_type).data
        return data


class ProviderMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'document_type',
            'document',
            'phone',
            'address',
            'is_active'
        ]


class PrizingTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizingTable
        fields = [
            'id',
            'provider',
            'product',
            'currency',
            'cost',
            'is_active'
        ]

    def to_representation(self, instance):
        data = super(PrizingTableSerializer, self).to_representation(instance)
        if instance.provider:
            data['provider'] = ProviderMiniSerializer(instance=instance.provider).data
        if instance.product:
            data['product'] = ProductMiniSerializer(instance=instance.product).data
        if instance.currency:
            data['currency'] = CurrencySerializer(instance=instance.currency).data
        return data
