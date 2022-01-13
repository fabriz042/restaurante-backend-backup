from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum, F

from apps.accounts.models import Restaurant
from apps.client.models import Client
from apps.currency.models import Currency
from apps.hall.models import Table
from apps.menu.models import MenuItem
from apps.provider.models import Provider
from apps.warehouse.models import WarehouseMovement, Warehouse
from utils import number_to_letters


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


class PaymentDocument(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='payment_documents',
        null=False,
        verbose_name='Restaurante'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Documento de Pago"
        verbose_name_plural = "Documento de Pago"

    def __str__(self):
        return self.name


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
    payment_document = models.ForeignKey(
        PaymentDocument,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
        verbose_name='Documento de Pago'
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

    @property
    def sub_total_(self):
        mount = self.details.filter(is_active=True).aggregate(
            subtotal_total=Sum('subtotal')
        )
        subtotal = mount['subtotal_total'] if mount['subtotal_total'] else 0
        return subtotal

    @property
    def igv_(self):
        mount = self.details.filter(is_active=True).aggregate(
            igv_total=Sum('igv')
        )
        igv = mount['igv_total'] if mount['igv_total'] else 0
        return igv

    @property
    def operation_value(self):
        mount = self.details.filter(is_active=True).aggregate(
            subtotal_total=Sum('subtotal'), igv_total=Sum('igv')
        )
        subtotal = mount['subtotal_total'] if mount['subtotal_total'] else 0
        igv = mount['igv_total'] if mount['igv_total'] else 0
        return subtotal + igv

    @property
    def operation_value_as_letters(self):
        return number_to_letters(self.operation_value)

    @property
    def paid(self):
        mount = self.payments.all().aggregate(
            mount=Sum('mount')
        )
        return mount['mount'] if mount['mount'] else 0

    @property
    def debt(self):
        return self.operation_value - self.paid


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
    movement = models.OneToOneField(
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

    @property
    def quantity_abs(self):
        return abs(self.movement.quantity)

    class Meta:
        verbose_name = 'Detalle de Operacion'


class PurchaseDetail(OperationsDetail):
    pass


class Order(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='orders',
        null=False,
        verbose_name='Restaurante'
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Mesa',
        related_name='orders'
    )
    start_datetime = models.DateTimeField(
        null=False,
        verbose_name='Hora de Inicio'
    )
    end_datetime = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Hora de Fin'
    )
    waiter = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Mesero',
        related_name='orders'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        default=None,
        verbose_name='Tipo de moneda'
    )
    serie = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
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
        default=None,
        on_delete=models.SET_NULL,
        verbose_name='Tipo de Pago'
    )
    payment_document = models.ForeignKey(
        PaymentDocument,
        null=True,
        on_delete=models.SET_NULL,
        default=None,
        verbose_name='Documento de Pago'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Cliente'
    )

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    @property
    def total(self):
        mount = self.details.filter(is_active=True).aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )
        subtotal = mount['total'] if mount['total'] else 0
        return subtotal

    @property
    def igv(self):
        return float(self.total) - self.sub_total

    @property
    def sub_total(self):
        return float(self.total) / 1.18

    def total_as_letters(self):
        return number_to_letters(self.total)


class OrderDetail(models.Model):
    class State(models.IntegerChoices):
        MAKING = 0, 'Preparando'
        DELIVERED = 1, 'Entregado'
        QUEUED = 2, 'En Cola'

    header = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name='Cabecera'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='order_details',
        verbose_name='Item de Menú'
    )
    quantity = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        verbose_name='Cantidad'
    )
    state = models.IntegerField(
        choices=State.choices,
        verbose_name='Estado'
    )
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Precio Unitario'
    )
    movements = models.ManyToManyField(
        WarehouseMovement,
        related_name='order_details'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'

    @property
    def sub_total(self):
        return self.quantity * self.unit_price

    @property
    def prize_net(self):
        return float(self.unit_price)/1.18

    @property
    def igv(self):
        return float(self.unit_price) - self.prize_net


class Serie(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='series',
        null=False,
        verbose_name='Restaurante'
    )
    code = models.CharField(
        max_length=10,
        verbose_name='Código'
    )
    correlative = models.IntegerField(
        default=1,
        verbose_name='Correlativo'
    )
    payment_document = models.ForeignKey(
        PaymentDocument,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Documento de Pago',
        related_name='series'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'
