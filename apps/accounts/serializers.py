from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.accounts.models import Profile, Role, Restaurant


class RoleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = []
        extra_kwargs = {'permissions': {'write_only': False}}

    def to_representation(self, instance):
        role = Role.objects.get(id=instance.id)
        return {
            'id': role.id,
            'role_name': role.role_name
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'email', 'username', 'password', 'groups'
        ]
        validate_password = make_password

    extra_kwargs = {'groups': {'required': False}}

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['groups'] = RoleMiniSerializer(instance.groups, many=True).data
        return data


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()

    class Meta:
        model = Permission
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'phone'
        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role_name', 'permissions']

    def to_representation(self, instance):
        data = super(RoleSerializer, self).to_representation(instance)
        data['permissions'] = PermissionSerializer(instance.permissions, many=True).data
        return data


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'ruc', 'picture', 'email', 'business_name', 'phone']
        read_only_fields = ('picture', 'id')


class RestaurantPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['picture']
