from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

# Create your views here.
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
        return PrizingTable.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyPrizingTableAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = PrizingTableSerializer

    def get_queryset(self):
        return PrizingTable.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
