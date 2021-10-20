from rest_framework import generics

# Create your views here.
from apps.operations.models import PaymentType, Purchase
from apps.operations.serializers import PaymentTypeSerializer, PurchaseSerializer
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

    def get_queryset(self):
        return Purchase.objects.select_related(
            'payment_type', 'currency'
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
