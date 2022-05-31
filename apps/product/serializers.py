from rest_framework import serializers
from django.db.models import Sum
from apps.menu.models import MenuProduct, MenuCategory
from apps.product.models import Brand, ProductCategory, MeasurementUnit, Product
from apps.warehouse.models import Warehouse, WarehouseMovement


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
    sell_price = serializers.DecimalField(
        decimal_places=2,
        max_digits=10,
        source='menu_products.sell_price'
    )
    default_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.filter(is_active=True),
        source='menu_products.warehouse'
    )
    menu_category = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.filter(is_active=True),
        source='menu_products.category'
    )
    menu_products = serializers.PrimaryKeyRelatedField(
        queryset=MenuProduct.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'measurement_unit',
            'category',
            'brand',
            'net_weight',
            'gross_weight',
            'yield_percentage',
            'is_active',
            'menu_products',
            'sell_price',
            'default_warehouse',
            'menu_category'
        ]

    def update(self, instance, validated_data):
        menu_products_data = validated_data['menu_products']
        del validated_data['menu_products']
        instance = super(ProductSerializer, self).update(instance, validated_data)
        for attr_name in menu_products_data:
            setattr(instance.menu_products, attr_name, menu_products_data[attr_name])
        instance.menu_products.save()
        return instance

    def create(self, validated_data):
        menu_products_data = validated_data['menu_products']
        del validated_data['menu_products']
        instance = super(ProductSerializer, self).create(validated_data)
        menu_products_data['restaurant'] = instance.restaurant
        menu_products_data['product'] = instance
        menu_product = MenuProduct()
        for attr_name in menu_products_data:
            setattr(menu_product, attr_name, menu_products_data[attr_name])
        menu_product.save()
        return instance

    def to_representation(self, instance):
        if not hasattr(instance, 'menu_products'):
            MenuProduct.objects.create(
                product=instance,
                restaurant=instance.restaurant
            )
        data = super(ProductSerializer, self).to_representation(instance)
        if instance.measurement_unit:
            data['measurement_unit'] = MeasurementUnitSerializer(instance.measurement_unit).data
        if instance.category:
            data['category'] = ProductCategorySerializer(instance.category).data
        if instance.brand:
            data['brand'] = BrandSerializer(instance.brand).data
        if instance.menu_products.warehouse:
            from apps.warehouse.serializers import WarehouseSerializer
            data['default_warehouse'] = WarehouseSerializer(instance.menu_products.warehouse).data
        if instance.menu_products.category:
            from apps.menu.serializers import MenuCategorySerializer
            data['menu_category'] = MenuCategorySerializer(instance.menu_products.category).data
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

    def to_representation(self, instance):
        data = super(ProductMiniSerializer, self).to_representation(instance)
        stock = WarehouseMovement.objects.filter(is_active=True, product_id=instance.id).aggregate(Sum('quantity'))['quantity__sum']
        data['stock'] = stock if stock else 0
        return data
