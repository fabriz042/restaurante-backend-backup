from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.recipe.models import Recipe, RecipeDetail
from apps.recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateRecipeAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            'details', 'details__product', 'details__product__measurement_unit',
            'details__product__category', 'details__product__brand'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class RetrieveUpdateDestroyRecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            'details', 'details__product', 'details__product__measurement_unit',
            'details__product__category', 'details__product__brand'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListCreateRecipeDetailAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RecipeDetailSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'recipe'
    ]

    def get_queryset(self):
        return RecipeDetail.objects.select_related(
            'product', 'product__measurement_unit', 'product__category', 'product__brand'
        ).filter(
            is_active=True,
            recipe__restaurant__user_profiles__user=self.request.user
        )


class RetrieveUpdateDestroyRecipeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RecipeDetailSerializer

    def get_queryset(self):
        return RecipeDetail.objects.select_related(
            'product', 'product__measurement_unit', 'product__category', 'product__brand'
        ).filter(
            is_active=True,
            recipe__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
