from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant
from apps.product.models import Product


class Warehouse(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='warehouses'
    )
    name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Nombre'
    )
    address = models.CharField(
        max_length=1500,
        null=True,
        blank=True,
        verbose_name='Dirección'
    )
    is_main = models.BooleanField(
        default=False,
        null=False,
        verbose_name='Almacen Principal'
    )

    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Alamacenes'


class WarehouseMovement(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='movements'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Producto',
        related_name='movements'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Almacen',
        related_name='movements'
    )
    quantity = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        null=False,
        verbose_name='Cantidad'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Movimiento de Almacen'
        verbose_name_plural = 'Movimientos de Almacen'