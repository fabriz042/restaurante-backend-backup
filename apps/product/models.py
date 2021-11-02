from django.db import models

# Create your models here.
from django.db.models import Sum, Avg

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
    net_weight = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=False,
        default=0,
        verbose_name='Peso Neto'
    )
    gross_weight = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=False,
        default=0,
        verbose_name='Peso Bruto'
    )
    yield_percentage = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=False,
        default=0,
        verbose_name='Porcentaje de Rendimiento'
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.yield_percentage = self.net_weight / self.gross_weight
        super(Product, self).save(force_insert, force_update, using, update_fields)

    @property
    def average_real_cost(self):
        cost = self.detail_operation.aggregate(total=Avg('detail_operation__subtotal'))
        if cost['total']:
            return cost['total']
        return 0

    @property
    def detail_operation(self):
        return self.movements.filter(is_active=True, detail_operation__is_active=True).exclude(detail_operation=None)

    @property
    def average_igv(self):
        igv = self.detail_operation.aggregate(total=Avg('detail_operation__igv'))
        if igv['total']:
            return igv['total']
        return 0

    @property
    def average_cost(self):
        return self.average_real_cost + self.average_igv

    @property
    def clean_price(self):
        if self.yield_percentage == 0:
            return self.average_cost
        return self.average_cost/self.yield_percentage
