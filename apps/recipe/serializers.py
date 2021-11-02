from rest_framework import serializers

from apps.product.serializers import ProductSerializer
from apps.recipe.models import Recipe, RecipeDetail


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
    details = RecipeDetailSerializer(many=True, context='self.context')

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'details',
            'is_active'
        ]
        read_only_fields = ('is_active', 'id', 'details')

    def to_representation(self, instance):
        data = super(RecipeSerializer, self).to_representation(instance)
        data['food_cost'] = serializers.DecimalField(
            max_digits=8,
            decimal_places=2
        ).to_representation(instance.food_cost)
        return data
