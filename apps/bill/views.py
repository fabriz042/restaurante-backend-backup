import io
from pathlib import Path

import OpenSSL.crypto
import pem
import requests
from OpenSSL import crypto
from django.core.files.base import ContentFile
from rest_framework import generics, status

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from zeep import Client
from zeep.transports import Transport

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
        bill.write_xml()
        bill.write_zip()
        settings = bill.order.restaurant.billing_settings
        # wsdl_url = 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl'
        wsdl_url = 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl'

        username = '{}{}'.format(
            bill.order.restaurant.ruc,
            settings.second_user
        )
        adapter = BillToXMLSenderAdapter(bill, settings)
        content = adapter.build_file()

        bill.send_file.save(bill.filename + '.xml', io.StringIO(content))

        f = open(bill.zip_file.path, 'rb')
        data_file = f.read()
        filename = Path(bill.zip_file.path).name

        password = settings.second_user_password
        session = requests.session()

        session.auth = requests.auth.HTTPBasicAuth(username, password)

        client = self.connect(wsdl_url, session)

        response = self.send_bill(client, filename, data_file)

        data = ContentFile(response)
        bill.response_zip_file.save(bill.filename + '.zip', data)

        return Response(
            self.get_serializer_class()(bill, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def send_bill(client, filename, data_file):
        try:
            response = client.service.sendBill(
                filename,
                data_file
            )
            return response
        except Exception as e:
            raise ValidationError({
                'detail': str(e)
            })

    @staticmethod
    def connect(wsdl_url, session):
        try:
            client = Client(
                wsdl_url,
                transport=Transport(
                    session=session,
                    timeout=(5, 30)
                ), service_name='billService',
                port_name='BillServicePort'
            )
            return client
        except Exception as e:
            raise ValidationError({
                'detail': str(e)
            })

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
