from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant
from apps.document_type.models import DocumentType


class Client(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='clients'
    )
    name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Nombre'
    )
    document_type = models.ForeignKey(
        DocumentType,
        null=True,
        default=None,
        on_delete=models.RESTRICT,
        related_name='clients',
        verbose_name='Tipo de Documento'
    )
    document = models.CharField(
        max_length=25,
        null=True,
        default=None,
        verbose_name='Documento'
    )
    phone = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        default=None,
        verbose_name='Telefóno'
    )
    address = models.CharField(
        max_length=250,
        blank=False,
        null=True,
        default=None,
        verbose_name='Dirección'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clientes'
