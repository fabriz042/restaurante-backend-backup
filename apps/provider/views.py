from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.operations.models import Purchase
from apps.operations.serializers import PurchaseSerializer
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.provider.models import Provider, PrizingTable
from apps.provider.serializers import ProviderSerializer, PrizingTableSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateProviderAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = ProviderSerializer

    def get_queryset(self):
        return Provider.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class RetrieveUpdateDestroyProviderAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = ProviderSerializer

    def get_queryset(self):
        return Provider.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListCreatePrizingTableAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = PrizingTableSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'provider',
        'product',
        'currency',
    ]

    def get_queryset(self):
        return PrizingTable.objects.select_related(
            'provider', 'product', 'currency'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyPrizingTableAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = PrizingTableSerializer

    def get_queryset(self):
        return PrizingTable.objects.select_related(
            'provider', 'product', 'currency'
        ).filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AccountListAPIView(generics.ListCreateAPIView):
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


class PayProviderAPIView(APIView):
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Payment.objects.filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def post(self, request):
        provider = get_object_or_404(Provider, id=self.request.data['provider'])
        purchases = Purchase.objects.select_related(
            'payment_type', 'currency', 'provider'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            provider=provider
        ).order_by('issue_date')
        mount = self.request.data['mount']
        payments = []
        for purchase in purchases:
            if mount == 0:
                break
            else:
                debt = purchase.debt
                if debt > 0:
                    to_pay = min(mount, debt)
                    payment = Payment(
                        operation=purchase,
                        mount=to_pay
                    )
                    payment.save()
                    payments.append(payment)
                    mount -= to_pay
        return Response(
            data={
                'rest': mount,
                'payments': PaymentSerializer(payments, many=True).data
            }
        )


