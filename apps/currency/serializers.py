from rest_framework import serializers

from apps.currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'name',
            'symbol',
            'code',
            'is_active'
        ]
