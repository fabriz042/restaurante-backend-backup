from django.shortcuts import render


# Create your views here.
from rest_framework import generics

from apps.hall.models import Hall, Table
from apps.hall.serializers import HallSerializer, TableSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class HallListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HallSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Hall.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class HallRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HallSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Hall.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TableCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TableSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Table.objects.filter(
            is_active=True,
            hall__restaurant__user_profiles__user=self.request.user
        )


class TableRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TableSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Table.objects.filter(
            is_active=True,
            hall__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
