from rest_framework import serializers

from apps.document_type.serializers import DocumentTypeSerializer
from apps.provider.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'id',
            'name',
            'document_type',
            'document',
            'phone',
            'address',
            'is_active'
        ]

    def to_representation(self, instance):
        data = super(ProviderSerializer, self).to_representation(instance)
        data['document_type'] = DocumentTypeSerializer(instance=instance.document_type).data
        return data
