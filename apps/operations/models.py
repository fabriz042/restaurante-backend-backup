from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant
from apps.currency.models import Currency
from apps.provider.models import Provider
from apps.warehouse.models import WarehouseMovement


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


class Operation(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='operations',
        null=False,
        verbose_name='Restaurante'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operations',
        verbose_name='Tipo de moneda'
    )
    sub_total = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=False,
        default=0,
        verbose_name='SubTotal'
    )
    serie = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='Serie'
    )
    correlative = models.IntegerField(
        default=0,
        null=True,
        verbose_name='Correlativo'
    )
    payment_type = models.ForeignKey(
        PaymentType,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Tipo de Pago'
    )
    issue_date = models.DateField(
        null=False,
        verbose_name='Fecha'
    )
    igv = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=False,
        default=0,
        verbose_name='IGV'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    @property
    def total(self):
        return self.sub_total + self.igv

    class Meta:
        verbose_name = 'Operación'
        verbose_name_plural = 'Operaciones'


class Purchase(Operation):
    provider = models.ForeignKey(
        Provider,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
        verbose_name='Proveedor',
    )

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class OperationsDetail(models.Model):
    operation = models.ForeignKey(
        Operation,
        default=None,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='Operation'
    )
    subtotal = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        null=False,
        verbose_name='Sub Total'
    )
    unitary_value = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        null=False,
        verbose_name='Valor Unitario'
    )
    igv = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        null=False,
        verbose_name='IGV'
    )
    movement = models.ForeignKey(
        WarehouseMovement,
        null=False,
        on_delete=models.CASCADE,
        related_name='detail_operation',
        verbose_name='Movimiento'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Detalle de Operacion'


class PurchaseDetail(OperationsDetail):
    pass
