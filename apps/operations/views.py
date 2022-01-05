import datetime

import pytz
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

# Create your views here.
from rest_framework.response import Response

from apps.hall.models import Table
from apps.menu.models import MenuProduct, MenuRecipe
from apps.operations.models import PaymentType, Purchase, PurchaseDetail, Order, OrderDetail
from apps.operations.serializers import PaymentTypeSerializer, PurchaseSerializer, PurchaseDetailSerializer, \
    OrderSerializer, OrderDetailSerializer, OrderExtendedSerializer
from apps.warehouse.models import WarehouseMovement
from apps.warehouse.serializers import WarehouseMovementSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class PaymentTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PaymentType.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PaymentTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PaymentType.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PurchaseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'payment_type', 'currency', 'provider'
    ]

    def get_queryset(self):
        return Purchase.objects.select_related(
            'payment_type', 'currency', 'provider'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PurchaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Purchase.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PurchaseDetailListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PurchaseDetailSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'operation'
    ]

    def get_queryset(self):
        return PurchaseDetail.objects.select_related(
            'movement', 'movement__product'
        ).filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        movement_data = self.request.data
        movement_serializer = WarehouseMovementSerializer(data=movement_data)
        movement_serializer.is_valid(raise_exception=True)
        serializer.save(
            movement=movement_serializer.save(restaurant=self.request.user.profile.restaurant)
        )


class PurchaseDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseDetailSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PurchaseDetail.objects.select_related(
            'movement', 'movement__product'
        ).filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        instance.movement.is_active = False
        instance.movement.save()

    def perform_update(self, serializer):
        movement_data = self.request.data
        movement_serializer = WarehouseMovementSerializer(
            instance=self.get_object().movement,
            data=movement_data
        )
        movement_serializer.is_valid(raise_exception=True)
        movement = movement_serializer.save()
        serializer.save()


class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter'
    ]

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        instance = serializer.save(restaurant=self.request.user.profile.restaurant)
        instance.table.state = Table.State.BUSSY
        instance.table.save()


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def perform_update(self, serializer):
        prev_instance = self.get_object()
        instance = serializer.save()
        if not prev_instance.end_datetime and instance.end_datetime:
            instance.table.state = Table.State.FREE
            instance.table.save()


class OrderDetailListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'header'
    ]

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.unit_price = instance.menu_item.sell_price
        instance.save()


class OrderDetailRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        instance.movements.all().update(is_active=False)


class OrderDetailMakeMovementsAPIViews(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        is_product = MenuProduct.objects.filter(id=instance.menu_item.id)
        is_recipe = MenuRecipe.objects.filter(id=instance.menu_item.id)
        movements = []
        if len(is_product) > 0:
            movement = WarehouseMovement(
                restaurant=instance.header.restaurant,
                warehouse=instance.menu_item.warehouse,
                quantity=instance.quantity,
                product=is_product[0].product
            )
            movement.save()
            instance.movements.add(movement)
            instance.save()
        if len(is_recipe) > 0:
            for recipe_detail in is_recipe[0].recipe.details.all():
                movement = WarehouseMovement(
                    restaurant=instance.header.restaurant,
                    warehouse=instance.menu_item.warehouse,
                    quantity=instance.quantity * recipe_detail.quantity,
                    product=recipe_detail.product
                )
                movement.save()
                instance.movements.add(movement)
                instance.save()
                movements.append(movement)
        return Response(WarehouseMovementSerializer(movements, many=True).data)


class OpenedOrderListAPIView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderExtendedSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter'
    ]

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).prefetch_related('details').filter(
            end_datetime=None,
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )


class OrderExtendedListAPIView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderExtendedSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter'
    ]

    def get_queryset(self):
        details_state = self.request.query_params.get('details__state', None)
        queryset = Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            # end_datetime=None,
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )
        if details_state:
            queryset = queryset.filter(details__state=details_state).distinct()
        return queryset
