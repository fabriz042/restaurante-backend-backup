from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant


class PaymentType(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='payment_types',
        null=False,
        verbose_name='Restaurante'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Nombre"
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"
