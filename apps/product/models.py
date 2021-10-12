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


class MeasurementUnit(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='measurement_units'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Nombre'
    )
    code = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Código'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"


class Product(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurant',
        related_name='products'
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Nombre'
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        null=False,
        on_delete=models.RESTRICT,
        verbose_name='Unidad de Medida',
        related_name='products'
    )
    category = models.ForeignKey(
        ProductCategory,
        null=False,
        on_delete=models.RESTRICT,
        verbose_name='Categoría de Producto',
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        default=None,
        on_delete=models.RESTRICT,
        verbose_name='Marca de Producto',
        related_name='products'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
