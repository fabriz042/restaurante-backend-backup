from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group, Permission

from apps.accounts.models import Restaurant, Profile, Settings, Role
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin, GroupAdmin

from apps.currency.models import Currency
from apps.document_type.models import DocumentType
from apps.product.models import Brand, ProductCategory, MeasurementUnit, Product
from apps.provider.models import Provider, PrizingTable
from apps.warehouse.models import Warehouse, WarehouseMovement


class WarehouseMovementTabularInLine(admin.TabularInline):
    model = WarehouseMovement
    extra = 1


class WarehouseTabularInline(admin.TabularInline):
    model = Warehouse
    extra = 1


class CurrencyTabularInline(admin.TabularInline):
    model = Currency
    extra = 1


class PrizingTableTabularInline(admin.TabularInline):
    model = PrizingTable
    extra = 1


class ProfileTabularInline(admin.TabularInline):
    model = Profile
    extra = 1
    fields = [
        'user',
        'phone'
    ]


class ProfileStackedInline(admin.StackedInline):
    model = Profile


class SettingsStackedInLine(admin.StackedInline):
    model = Settings


class RoleTabularInline(admin.TabularInline):
    model = Role
    extra = 1

    fields = [
        'role_name',
        'permissions'
    ]


class DocumentTypeTabularInline(admin.TabularInline):
    model = DocumentType
    extra = 1


class ProviderTabularInline(admin.TabularInline):
    model = Provider
    extra = 1

    fields = [
        'name',
        'document_type',
        'document',
        'is_active'
    ]


class BrandTabularInline(admin.TabularInline):
    model = Brand
    extra = 1


class ProductCategoryTabularInline(admin.TabularInline):
    model = ProductCategory
    extra = 1


class MeasurementUnitTabularInline(admin.TabularInline):
    model = MeasurementUnit
    extra = 1


class ProductTabularInline(admin.TabularInline):
    model = Product
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    """PartyCompanyAdmin Class"""
    inlines = [
        ProfileTabularInline,
        SettingsStackedInLine,
        RoleTabularInline,
        DocumentTypeTabularInline,
        ProviderTabularInline,
        BrandTabularInline,
        ProductCategoryTabularInline,
        MeasurementUnitTabularInline,
        ProductTabularInline,
        CurrencyTabularInline,
        PrizingTableTabularInline,
        WarehouseTabularInline,
        WarehouseMovementTabularInLine
    ]
    list_display = [
        'id',
        'name',
        'address',
        'ruc',
        'state',
        'owner'
    ]
    list_filter = [
        'state'
    ]
    search_fields = [
        'name',
        'business_name'
    ]


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileStackedInline]
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active'
    ]


class PermissionStackedInLine(admin.StackedInline):
    model = Permission


class RoleAdmin(GroupAdmin):
    """PartyCompanyAdmin Class"""
    inlines = [
        #    PermissionStackedInLine
    ]
    list_display = [
        'id',
        'role_name',
        'restaurant'
    ]
    list_filter = [
        'name',
        'restaurant'
    ]
    search_fields = [
        'name',
        'restaurant'
    ]


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
