from rest_framework import serializers

from apps.operations.models import PaymentType


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'is_active']
