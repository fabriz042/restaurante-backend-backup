from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.menu.models import MenuCategory, MenuProduct, MenuRecipe
from apps.menu.serializers import MenuCategorySerializer, MenuProductSerializer, MenuRecipeSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class MenuCategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return MenuCategory.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class MenuCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return MenuCategory.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class MenuProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuProductSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'category',
        'product'
    ]

    def get_queryset(self):
        return MenuProduct.objects.select_related(
            'category', 'product'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class MenuProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuProductSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return MenuProduct.objects.select_related(
            'category', 'product'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class MenuRecipeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuRecipeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'category',
        'recipe'
    ]

    def get_queryset(self):
        return MenuRecipe.objects.select_related(
            'category', 'recipe'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            recipe__is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class MenuRecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuRecipeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return MenuRecipe.objects.select_related(
            'category', 'recipe'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            recipe__is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
