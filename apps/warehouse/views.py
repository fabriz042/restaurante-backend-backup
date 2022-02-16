from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from apps.product.models import Product
from apps.warehouse.models import Warehouse, WarehouseMovement
from apps.warehouse.serializers import WarehouseSerializer, WarehouseMovementSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateWarehouseAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyWarehouseAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListCreateWarehouseMovementAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseMovementSerializer

    def get_queryset(self):
        return WarehouseMovement.objects.select_related(
            'product', 'warehouse'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyWarehouseMovementAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseMovementSerializer

    def get_queryset(self):
        return WarehouseMovement.objects.select_related(
            'product', 'warehouse'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class WarehouseStockAPIView(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def retrieve(self, request, *args, **kwargs):
        warehouse = self.get_object()
        stocks = warehouse.movements.filter(is_active=True).values('product').annotate(
            stock=Sum('quantity')
        ).order_by('stock')
        data = []
        for item in stocks:
            product = Product.objects.get(id=item['product'])
            data.append({
                'id': product.id,
                'name': product.name,
                'stock': item['stock']
            })
        return Response(data)
