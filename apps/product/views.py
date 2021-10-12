from rest_framework import generics

# Create your views here.
from apps.product.models import Brand
from apps.product.serializers import BrandSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateBrandAPIView(generics.ListCreateAPIView):
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Brand.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PerformUpdateDestroyBrandAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Brand.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

