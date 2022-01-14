import io

import pem
from OpenSSL import crypto
from rest_framework import generics


# Create your views here.
from rest_framework.response import Response

from apps.bill.models import BillingSetting
from apps.bill.serializers import BillingSettingSerializer, BillSettingsCertificateSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class BillingSettingsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = BillingSettingSerializer
    queryset = BillingSetting.objects.all()

    def get_object(self):
        return BillingSetting.objects.get_or_create(
            restaurant=self.request.user.profile.restaurant
        )[0]


class BillingSettingsCertificateAPIView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = BillSettingsCertificateSerializer
    queryset = BillingSetting.objects.all()

    def get_object(self):
        return BillingSetting.objects.get_or_create(
            restaurant=self.request.user.profile.restaurant
        )[0]

    def perform_update(self, serializer):
        instance = serializer.save()
        p12 = crypto.load_pkcs12(
            instance.sunat_certificate.read(),
            instance.password_certificate
        )
        private_key = crypto.dump_privatekey(
            crypto.FILETYPE_PEM,
            p12.get_privatekey()
        )
        certificate = crypto.dump_certificate(
            crypto.FILETYPE_PEM,
            p12.get_certificate()
        )

        private_key_pem = pem.parse(private_key)
        certificate_key_pem = pem.parse(certificate)

        private_key_io = io.BytesIO(private_key_pem[0].as_bytes())
        instance.certificate_private_key.save(
            'private_key.key',
            private_key_io
        )
        certificate_io = io.BytesIO(certificate_key_pem[0].as_bytes())
        instance.certificate_pem.save(
            'certificate.pem',
            certificate_io
        )




