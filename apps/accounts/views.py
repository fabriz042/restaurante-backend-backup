from django.contrib.auth.models import User, Permission
from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Restaurant, Profile, Role
from apps.accounts.serializers import UserSerializer, PermissionSerializer, ProfileSerializer, \
    RoleSerializer, RestaurantSerializer, RestaurantPictureSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        restaurant = Restaurant()
        restaurant.save()
        profile = Profile(user=instance, restaurant=restaurant)
        profile.save()
        role = Role(role_name='Administrador', restaurant=restaurant)
        role.save()
        role.permissions.add(*(Permission.objects.all()))
        role.save()
        instance.groups.add(role)
        instance.set_password(self.request.data['password'])
        instance.save()


class ListUserAuthPermissionsAPIView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_permissions = self.request.user.user_permissions.all()
        group_permissions = Permission.objects.filter(group__user=self.request.user)
        return user_permissions | group_permissions

    def list(self, request, *args, **kwargs):
        return Response(
            data=self.get_queryset().values_list('codename', flat=True)
        )


class RetrieveUpdateUserAuthAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RetrieveUpdateProfileAuthAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ListCreateUserAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return User.objects.filter(profile__restaurant=self.request.user.profile.restaurant, is_active=True)

    def perform_create(self, serializer):
        instance = serializer.save()
        restaurant = self.request.user.profile.restaurant
        profile = Profile(user=instance, restaurant=restaurant)
        profile.save()
        instance.set_password(self.request.data['password'])
        instance.save()


class RetrieveUpdateDestroyUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return User.objects.filter(profile__restaurant=self.request.user.profile.restaurant, is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ListCreateRoleAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(restaurant=self.request.user.profile.restaurant)

    def perform_create(self, serializer):
        restaurant = self.request.user.profile.restaurant
        serializer.save(restaurant=restaurant)


class RetrieveUpdateDestroyRoleAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(restaurant=self.request.user.profile.restaurant)


class ListPermissionAPIView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = PermissionSerializer

    def get_queryset(self):
        return Permission.objects.all().order_by('content_type')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        current_item = None
        serialized_data = self.get_serializer_class()(queryset, many=True).data
        for item in serialized_data:
            if not current_item:
                current_item = item['content_type']
                current_item['permissions'] = [{
                    'id': item['id'],
                    'name': item['name'],
                    'codename': item['codename']
                }]
                data.append(current_item)
            elif current_item['id'] == item['content_type']['id']:
                current_item['permissions'].append({
                    'id': item['id'],
                    'name': item['name'],
                    'codename': item['codename']
                })
            else:
                current_item = item['content_type']
                current_item['permissions'] = [{
                    'id': item['id'],
                    'name': item['name'],
                    'codename': item['codename']
                }]
                data.append(current_item)
        return Response(data)



class RestaurantRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_object(self):
        return self.request.user.profile.restaurant


class RestaurantPictureRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = RestaurantPictureSerializer
    queryset = Restaurant.objects.all()

    def get_object(self):
        return self.request.user.profile.restaurant
