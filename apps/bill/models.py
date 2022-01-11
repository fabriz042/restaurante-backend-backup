from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant


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
        max_length=10,
        default="",
        verbose_name='Contraseña Segundo Usuario SOL'
    )

    class Meta:
        verbose_name = 'Configuración de Facturación'
        verbose_name_plural = 'Configuraciones de Facturación'




