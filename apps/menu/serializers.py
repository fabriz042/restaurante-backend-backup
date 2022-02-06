from rest_framework import serializers

from apps.menu.models import MenuCategory, MenuProduct, MenuRecipe, MenuItem
from apps.product.serializers import ProductMiniSerializer
from apps.recipe.serializers import RecipeMiniSerializer


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = [
            'id', 'name', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')


class MenuProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuProduct
        fields = [
            'id', 'category', 'sell_price', 'product', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(MenuProductSerializer, self).to_representation(instance)
        if instance.category:
            data['category'] = MenuCategorySerializer(instance.category).data
        if instance.product:
            data['product'] = ProductMiniSerializer(instance.product).data
        return data


class MenuRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuRecipe
        fields = [
            'id', 'category', 'sell_price', 'recipe', 'is_active', 'daily_quantity'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(MenuRecipeSerializer, self).to_representation(instance)
        if instance.category:
            data['category'] = MenuCategorySerializer(instance.category).data
        if instance.recipe:
            data['recipe'] = RecipeMiniSerializer(instance.recipe).data
        return data


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def to_representation(self, instance):
        is_product = MenuProduct.objects.filter(id=instance.id)
        is_recipe = MenuRecipe.objects.filter(id=instance.id)
        if len(is_product) > 0:
            return MenuProductSerializer(is_product[0]).data
        if len(is_recipe) > 0:
            return MenuRecipeSerializer(is_recipe[0]).data
        return None
