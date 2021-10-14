from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant


class Currency(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='currencies',
        null=False,
        verbose_name='Restaurante'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Nombre"
    )
    symbol = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name="Simbolo"
    )
    code = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        default='',
        verbose_name="Código"
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = "Tipo de Moneda",
        verbose_name_plural = "Tipos de Moneda"
