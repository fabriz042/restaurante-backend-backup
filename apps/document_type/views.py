from rest_framework import generics

# Create your views here.
from apps.document_type.models import DocumentType
from apps.document_type.serializers import DocumentTypeSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class ListCreateDocumentTypeAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = DocumentTypeSerializer

    def get_queryset(self):
        return DocumentType.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)


class RetrieveEditDestroyDocumentTypeAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = DocumentTypeSerializer

    def get_queryset(self):
        return DocumentType.objects.filter(
            is_active=True,
            restaurant=self.request.user.profile.restaurant
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
