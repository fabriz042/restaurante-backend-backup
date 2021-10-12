from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant


class Brand(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='brands'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Nombre'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"


class ProductCategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='product_categories'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Nombre'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Producto"
