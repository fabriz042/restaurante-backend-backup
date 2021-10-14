from rest_framework import serializers

from apps.product.models import Brand, ProductCategory, MeasurementUnit, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'is_active'
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'name',
            'is_active'
        ]


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = [
            'id',
            'name',
            'code',
            'is_active'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'measurement_unit',
            'category',
            'brand',
            'is_active'
        ]

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        if instance.measurement_unit:
            data['measurement_unit'] = MeasurementUnitSerializer(instance.measurement_unit).data
        if instance.category:
            data['category'] = ProductCategorySerializer(instance.category).data
        if instance.brand:
            data['brand'] = BrandSerializer(instance.brand).data
        return data


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'measurement_unit',
            'category',
            'brand',
            'is_active'
        ]
