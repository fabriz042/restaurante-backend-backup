import io
from pathlib import Path

import OpenSSL.crypto
import pem
import requests
from OpenSSL import crypto
from django.core.files.base import ContentFile
from rest_framework import generics, status
from apps.bill.services import Services
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from zeep import Client
from zeep.wsse import UsernameToken

from apps.bill.adapters import BillToXMLSenderAdapter
from apps.bill.models import BillingSetting, BillOrder
from apps.bill.serializers import BillingSettingSerializer, BillSettingsCertificateSerializer, BillOrderSerializer
from apps.operations.models import Order
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
        try:
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
        except OpenSSL.crypto.Error as err:
            raise ValidationError({
                'detail': 'Contraseña no corresponde a certificado'
            })


class BillOrderServiceAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    queryset = BillOrder.objects.all()
    serializer_class = BillOrderSerializer

    def get_object(self):
        pk = int(self.request.parser_context.get('kwargs')['pk'])
        order = get_object_or_404(
            Order.objects.filter(
                restaurant=self.request.user.profile.restaurant),
            pk=pk
        )
        return BillOrder.objects.get_or_create(
            order=order
        )[0]

    def create(self, request, *args, **kwargs):
        bill = self.get_object()
        self.validate(bill)
        service = Services(bill.order.restaurant.billing_settings)
        try:
            data = service.send_bill(bill)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({'info': str(e)})

    @staticmethod
    def validate(bill: BillOrder):
        if not hasattr(bill.order.restaurant, 'billing_settings'):
            raise ValidationError({
                'detail': 'No se ha configurado la configuración de facturación'
            })
        if not bill.order.restaurant.billing_settings.certificate_pem:
            raise ValidationError({
                'detail': 'No se ha configurado el certificado para SUNAT'
            })
