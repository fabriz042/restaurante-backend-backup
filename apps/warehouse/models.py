from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant


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
