from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant
from apps.document_type.models import DocumentType


class Provider(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='providers'
    )
    name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Nombre'
    )
    document_type = models.ForeignKey(
        DocumentType,
        null=False,
        on_delete=models.RESTRICT,
        related_name='providers',
        verbose_name='Tipo de Documento'
    )
    document = models.CharField(
        max_length=25,
        null=False,
        verbose_name='Documento'
    )
    phone = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        verbose_name='Telefóno'
    )
    address = models.CharField(
        max_length=250,
        blank=False,
        null=True,
        verbose_name='Dirección'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
