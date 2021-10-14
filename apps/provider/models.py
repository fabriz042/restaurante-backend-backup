from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant
from apps.currency.models import Currency
from apps.document_type.models import DocumentType
from apps.product.models import Product


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


class PrizingTable(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='prices'
    )
    provider = models.ForeignKey(
        Provider,
        null=False,
        on_delete=models.RESTRICT,
        verbose_name="Proveedor",
        related_name='prices'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        on_delete=models.RESTRICT,
        verbose_name='Producto',
        related_name='prices'
    )
    currency = models.ForeignKey(
        Currency,
        null=False,
        on_delete=models.RESTRICT,
        verbose_name='Tipo de Moneda',
        related_name='prices'
    )
    cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name="Costo",
        null=False,
        default=0
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Tabla de Precios"
