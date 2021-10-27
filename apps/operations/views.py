from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

# Create your views here.
from apps.operations.models import PaymentType, Purchase, PurchaseDetail
from apps.operations.serializers import PaymentTypeSerializer, PurchaseSerializer, PurchaseDetailSerializer
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
