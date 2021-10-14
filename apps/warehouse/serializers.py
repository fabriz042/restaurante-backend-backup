from rest_framework import serializers

from apps.product.serializers import ProductMiniSerializer
from apps.warehouse.models import Warehouse, WarehouseMovement


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id',
            'name',
            'address',
            'is_main',
            'is_active'
        ]


class WarehouseMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseMovement
        fields = [
            'id',
            'product',
            'warehouse',
            'quantity',
            'is_active'
        ]

    def to_representation(self, instance):
        data = super(WarehouseMovementSerializer, self).to_representation(instance)
        if instance.product:
            data['product'] = ProductMiniSerializer(instance.product).data
        if instance.warehouse:
            data['warehouse'] = WarehouseSerializer(instance.warehouse).data
        return data
