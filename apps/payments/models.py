from django.db import models


# Create your models here.
from apps.operations.models import Operation


class Payment(models.Model):
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        null=False,
        related_name='payments',
        verbose_name='Operación'
    )
    mount = models.DecimalField(
        null=False,
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Monto'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )
