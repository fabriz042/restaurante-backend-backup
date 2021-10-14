from django.shortcuts import render


# Create your views here.
from rest_framework import generics

from apps.currency.models import Currency
from apps.currency.serializers import CurrencySerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateCurrencyAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyCurrencyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
