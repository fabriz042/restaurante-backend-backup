from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant
from apps.product.models import Product


class Recipe(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
        verbose_name="Nombre"
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        verbose_name="Activo"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Restaurante',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

    def __str__(self):
        return '{}\t|\t{}'.format(self.name, self.restaurant)

    @property
    def food_cost(self):
        food_cost = 0
        details = self.details.filter(is_active=True)
        for detail in details:
            food_cost += detail.total_cost
        return food_cost


class RecipeDetail(models.Model):
    quantity = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=False,
        default=0,
        verbose_name="Cantidad"
    )
    product = models.ForeignKey(
        Product,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Producto',
        related_name='recipes_details'
    )
    recipe = models.ForeignKey(
        Recipe,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Receta',
        related_name='details'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = 'Detalle de Receta'
        verbose_name_plural = 'Detalles de Receta'

    @property
    def total_cost(self):
        return self.quantity * self.product.clean_price
