from rest_framework import serializers

from apps.menu.models import MenuRecipe, MenuCategory
from apps.product.serializers import ProductSerializer
from apps.recipe.models import Recipe, RecipeDetail
from apps.warehouse.models import Warehouse


class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeDetail
        fields = [
            'id',
            'quantity',
            'product',
            'recipe',
            'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(RecipeDetailSerializer, self).to_representation(instance)
        if instance.product:
            data['product'] = ProductSerializer(instance=instance.product, context=self.context).data
            data['real_cost'] = instance.product.average_real_cost
            data['cost'] = instance.product.average_cost
            data['clean_price'] = serializers.DecimalField(
                max_digits=8,
                decimal_places=2
            ).to_representation(instance.product.clean_price)
            data['total'] = serializers.DecimalField(
                max_digits=8,
                decimal_places=2
            ).to_representation(instance.total_cost)
        return data


class RecipeSerializer(serializers.ModelSerializer):
    details = RecipeDetailSerializer(many=True, context='self.context', read_only=True)
    sell_price = serializers.DecimalField(
        decimal_places=2,
        max_digits=10,
        source='menu_recipe.sell_price'
    )
    default_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.filter(is_active=True),
        source='menu_recipe.warehouse'
    )
    menu_category = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.filter(is_active=True),
        source='menu_recipe.category'
    )
    menu_recipe = serializers.PrimaryKeyRelatedField(
        queryset=MenuRecipe.objects.filter(is_active=True),
        required=False
    )
    daily_quantity = serializers.IntegerField(
        source='menu_recipe.daily_quantity'
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'details',
            'is_active',
            'menu_recipe',
            'sell_price',
            'default_warehouse',
            'menu_category',
            'daily_quantity'
        ]
        read_only_fields = ('is_active', 'id', 'details')

    def update(self, instance, validated_data):
        menu_recipe_data = validated_data['menu_recipe']
        del validated_data['menu_recipe']
        instance = super(RecipeSerializer, self).update(instance, validated_data)
        for attr_name in menu_recipe_data:
            setattr(instance.menu_recipe, attr_name, menu_recipe_data[attr_name])
        instance.menu_recipe.save()
        return instance

    def create(self, validated_data):
        menu_recipe_data = validated_data['menu_recipe']
        del validated_data['menu_recipe']
        instance = super(RecipeSerializer, self).create(validated_data)
        menu_recipe_data['restaurant'] = instance.restaurant
        menu_recipe_data['recipe'] = instance
        menu_recipe = MenuRecipe()
        for attr_name in menu_recipe_data:
            print(attr_name)
            setattr(menu_recipe, attr_name, menu_recipe_data[attr_name])
        menu_recipe.save()
        return instance

    def to_representation(self, instance):
        if not hasattr(instance, 'menu_recipe'):
            MenuRecipe.objects.create(
                recipe=instance,
                restaurant=instance.restaurant
            )
        data = super(RecipeSerializer, self).to_representation(instance)
        data['food_cost'] = serializers.DecimalField(
            max_digits=8,
            decimal_places=2
        ).to_representation(instance.food_cost)
        if instance.menu_recipe.warehouse:
            from apps.warehouse.serializers import WarehouseSerializer
            data['default_warehouse'] = WarehouseSerializer(instance.menu_recipe.warehouse).data
        if instance.menu_recipe.category:
            from apps.menu.serializers import MenuCategorySerializer
            data['menu_category'] = MenuCategorySerializer(instance.menu_recipe.category).data
        return data


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'details',
            'is_active'
        ]
