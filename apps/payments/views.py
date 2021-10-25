from django.shortcuts import render


# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'operation'
    ]

    def get_queryset(self):
        return Payment.objects.filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Payment.objects.filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
