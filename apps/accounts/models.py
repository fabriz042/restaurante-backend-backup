import datetime

from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Restaurant(models.Model):
    class States(models.IntegerChoices):
        ACTIVE = 0, 'Activo'
        INACTIVATE = 1, 'Inactivo'

    name = models.CharField(
        max_length=400,
        blank=True,
        unique=False,
        null=True,
        verbose_name='Nombre'
    )
    address = models.CharField(
        max_length=360,
        blank=True,
        unique=False,
        null=True,
        verbose_name='Dirección'
    )
    ruc = models.CharField(
        max_length=13,
        blank=True,
        unique=False,
        null=True,
        verbose_name='RUC'
    )
    picture = models.ImageField(
        upload_to='restaurant/',
        blank=True,
        null=True,
        verbose_name='Figura'
    )
    # choice
    state = models.CharField(
        max_length=10,
        default=States.ACTIVE,
        choices=States.choices,
        blank=True,
        verbose_name='Estado'
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Correo Electronico'
    )
    business_name = models.CharField(
        max_length=160,
        blank=True,
        unique=False,
        null=True,
        verbose_name='Razón Social'
    )
    phone = models.CharField(
        max_length=200,
        blank=True,
        unique=False,
        null=True,
        verbose_name='Telefono'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=False,
        verbose_name='Propietario'
    )

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurante'


class Settings(models.Model):
    tasa = models.FloatField(
        verbose_name='TASA',
        default=0
    )
    edit_price = models.BooleanField(
        verbose_name='EDITAR PRECIO AGR',
        default=False
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Restaurante',
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    class Meta:
        app_label = 'auth'
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuraciones generales'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    phone = models.CharField(
        verbose_name='Teléfono',
        blank=True,
        max_length=20,
        unique=False,
        null=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        verbose_name='Restaurante',
        related_name='user_profiles'
    )

    class Meta:
        app_label = 'auth'
        verbose_name = 'Información de Usuario'
        verbose_name_plural = 'Información de Usuarios'


class Role(Group):
    role_name = models.CharField(
        default='',
        null=True,
        blank=False,
        verbose_name='Nombre',
        max_length=100
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        verbose_name='Restaurante'
    )

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        constraints = [
            models.UniqueConstraint(fields=['role_name', 'restaurant'], name='unique_rol_name')
        ]


@receiver(pre_save, sender=Role)
def role_is_saving(sender, instance, *args, **kwargs):
    instance.name = 'role_name_{}_restaurant_{}_datetime_{}'.format(
        instance.role_name,
        str(instance.restaurant.id),
        datetime.datetime.now()
    )
