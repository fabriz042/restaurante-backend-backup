from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group

from apps.accounts.models import Restaurant, Profile, Settings, Role
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


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


class RestaurantAdmin(admin.ModelAdmin):
    """PartyCompanyAdmin Class"""
    inlines = [
        ProfileTabularInline,
        SettingsStackedInLine,
        RoleTabularInline
    ]
    list_display = [
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


class RoleAdmin(admin.ModelAdmin):
    """PartyCompanyAdmin Class"""
    inlines = [
    ]
    list_display = [
        'name',
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
admin.site.unregister(Group)
admin.site.register(Role, RoleAdmin)
