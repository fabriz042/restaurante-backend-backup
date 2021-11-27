from django.db import models

# Create your models here.
from apps.accounts.models import Restaurant
from apps.product.models import Product
from apps.recipe.models import Recipe


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Restaurant',
        related_name='menu_categories'
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Nombre'
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Categoría de Menú'
        verbose_name_plural = 'Categorías de Menú'


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Restaurant',
        related_name='menu_items'
    )
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Category',
        related_name='menu_items'
    )
    sell_price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        verbose_name="Precio de Venta"
    )
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Activo'
    )

    class Meta:
        verbose_name = 'Item de Menú'
        verbose_name_plural = 'Item de Menú'


class MenuProduct(MenuItem):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Producto',
        related_name='menu_products'
    )

    class Meta:
        verbose_name = 'Menú Producto'
        verbose_name_plural = 'Menú  Producto'


class MenuRecipe(MenuItem):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Receta',
        related_name='menu_recipe'
    )

    class Meta:
        verbose_name = 'Menú Receta'
        verbose_name_plural = 'Menú  Receta'

