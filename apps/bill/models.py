import io
from zipfile import ZipFile

from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant
from apps.bill.adapters import BillOrderToXMLAdapter
from apps.bill.storage import OverwriteStorage
from apps.operations.models import Order


class BillingSetting(models.Model):
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='billing_settings',
        null=False,
        verbose_name='Restaurante'
    )
    user_sol = models.CharField(
        max_length=20,
        null=False,
        default='',
        verbose_name='Usuario SOL'
    )
    password_sol = models.CharField(
        max_length=30,
        null=False,
        default='',
        verbose_name='Clave SOL'
    )
    sunat_certificate = models.FileField(
        upload_to='sunat/certificates.p12',
        null=True,
        default=None,
        validators=[FileExtensionValidator(['p12'])],
        verbose_name='Certificado SUNAT'
    )
    password_certificate = models.CharField(
        max_length=50,
        null=True,
        default=None,
        verbose_name='Contraseña del Certificado'
    )
    certificate_pem = models.FileField(
        upload_to='sunat/certificates.pem',
        null=True,
        blank=True,
        verbose_name='Certificado PEM'
    )
    certificate_private_key = models.FileField(
        upload_to='sunat/certificates.keys',
        null=True,
        blank=True,
        verbose_name='Clave Privada de Certificado'
    )
    sunat_name = models.CharField(
        max_length=500,
        default="",
        verbose_name='Nombre en SUNAT'
    )
    location_code = models.CharField(
        max_length=10,
        default="0000",
        verbose_name='Código Ubigeo'
    )
    second_user = models.CharField(
        max_length=10,
        default="",
        verbose_name='Segundo Usuario SOL'
    )
    second_user_password = models.CharField(
        max_length=100,
        default="",
        verbose_name='Contraseña Segundo Usuario SOL'
    )

    class Meta:
        verbose_name = 'Configuración de Facturación'
        verbose_name_plural = 'Configuraciones de Facturación'


class Bill(models.Model):
    xml_file = models.FileField(
        storage=OverwriteStorage,
        upload_to='sunat/bill.xml/',
        default=None,
        blank=True
    )
    zip_file = models.FileField(
        storage=OverwriteStorage,
        upload_to='sunat/bill.zip/',
        default=None,
        blank=True
    )
    response_zip_file = models.FileField(
        storage=OverwriteStorage,
        upload_to='sunat/response.bill.zip/',
        default=None,
        blank=True
    )
    send_file = models.FileField(
        storage=OverwriteStorage,
        upload_to='sunat/bill.send/',
        default=None,
        blank=True
    )
    issue_datetime = models.DateTimeField(
        auto_now=True
    )

    def write_xml(self):
        pass


class BillOrder(Bill):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Pedido',
        null=False
    )

    def write_xml(self):
        adapter = BillOrderToXMLAdapter(self, self.order.restaurant.billing_settings)
        file_content = adapter.build_file()
        self.xml_file.save(
            self.filename + '.xml',
            io.BytesIO(file_content)
        )

    @property
    def filename(self):
        return '{}-01-{}'.format(
            self.order.restaurant.ruc,
            self.bill_name
        )

    @property
    def bill_name(self):
        return "{}-{}".format(
            self.order.serie,
            str(self.id).zfill(8)
        )

    def write_zip(self):
        self.zip_file.save(
            self.filename + '.zip',
            io.BytesIO(b'')
        )
        zip_obj = ZipFile(self.zip_file.path, 'w')
        zip_obj.write(self.xml_file.path, arcname=self.filename + '.xml')
        zip_obj.close()

