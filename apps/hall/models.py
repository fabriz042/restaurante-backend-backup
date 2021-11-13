from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant


class Hall(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Restaurant',
        related_name='hall'
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=300,
        verbose_name='Nombre'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Salón'
        verbose_name_plural = 'Salones'


class Table(models.Model):
    class State(models.IntegerChoices):
        FREE = 0, 'Libre'
        BUSSY = 1, 'Ocupado'
        WAITING_FOR = 2, 'Por desocuparse'
        RESERVED = 3, 'Reservado'

    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Salón',
        related_name='tables'
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=300,
        verbose_name='Nombre'
    )
    capacity = models.IntegerField(
        null=False,
        default=0,
        verbose_name='Capacidad'
    )
    state = models.IntegerField(
        null=False,
        choices=State.choices,
        default=0,
        verbose_name='Estado'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
