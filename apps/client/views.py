from django.shortcuts import render


# Create your views here.
from rest_framework import generics

from apps.client.models import Client
from apps.client.serializers import ClientSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateClientAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyClientAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
