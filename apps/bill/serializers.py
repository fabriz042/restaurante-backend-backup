from rest_framework import serializers

from apps.bill.models import BillingSetting


class BillingSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSetting
        fields = [
            'id', 'user_sol', 'password_sol', 'sunat_name',
            'location_code', 'second_user', 'second_user_password',
            'sunat_certificate', 'password_certificate'
        ]
        read_only_fields = ('sunat_certificate', 'id', 'password_certificate')


class BillSettingsCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSetting
        fields = [
            'id', 'sunat_certificate', 'password_certificate'
        ]
