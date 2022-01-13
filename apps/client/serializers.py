from rest_framework import serializers

from apps.client.models import Client
from apps.document_type.serializers import DocumentTypeSerializer


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'document_type', 'document', 'phone', 'address', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')

    def to_representation(self, instance):
        data = super(ClientSerializer, self).to_representation(instance)
        if instance.document_type:
            data['document_type'] = DocumentTypeSerializer(instance.document_type).data
        return data
