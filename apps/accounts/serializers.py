from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'email', 'username', 'password'
        ]
        validate_password = make_password


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
