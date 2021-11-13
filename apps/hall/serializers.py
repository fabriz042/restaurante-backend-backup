from rest_framework import serializers

from apps.hall.models import Hall, Table


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = [
            'id', 'name', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = [
            'id', 'name', 'hall', 'capacity', 'state', 'is_active'
        ]
        read_only_fields = ('is_active', 'id')
