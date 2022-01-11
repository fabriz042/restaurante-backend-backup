from rest_framework import serializers

from apps.bill.models import BillingSetting


class BillingSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSetting
        fields = [
            'id', 'user_sol', 'password_sol', 'sunat_name',
            'location_code', 'second_user', 'second_user_password'
        ]
