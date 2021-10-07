from django.db import models


# Create your models here.
from apps.accounts.models import Restaurant


class DocumentType(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Nombre',
        null=False
    )
    code = models.CharField(
        max_length=25,
        verbose_name='Código',
        null=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='document_types',
        null=False,
        verbose_name='Restaurante'
    )
    is_active = models.BooleanField(
        default=True,
        null=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'
