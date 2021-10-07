from rest_framework import serializers

from apps.document_type.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'code', 'is_active']
