import datetime

import pytz
from django.conf import settings
from django.db.models import Count, Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import MenuProduct, MenuItem, MenuRecipe
from apps.operations.models import OrderDetail, Order


class TopProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products_id = list(MenuProduct.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        ).values_list('id', flat=True))
        details = OrderDetail.objects.filter(
            is_active=True,
            header__is_active=True,
            header__restaurant__user_profiles__user=self.request.user,
            menu_item__id__in=products_id
        ).values('menu_item').annotate(sum=Sum("quantity")).order_by('-sum')
        details = details[:min(10, len(details))]
        return Response(
            data=self.serialize(details),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def serialize(details):
        data = []
        for detail in details:
            data.append({
                'id': detail['menu_item'],
                'name': MenuItem.objects.get(pk=detail['menu_item']).menu_item_name,
                'quantity': detail['sum']
            })
        return data


class TopRecipesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipes_id = list(MenuRecipe.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        ).values_list('id', flat=True))
        details = OrderDetail.objects.filter(
            is_active=True,
            header__is_active=True,
            header__restaurant__user_profiles__user=self.request.user,
            menu_item__id__in=recipes_id
        ).values('menu_item').annotate(sum=Sum("quantity")).order_by('-sum')
        details = details[:min(10, len(details))]
        return Response(
            data=self.serialize(details),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def serialize(details):
        data = []
        for detail in details:
            data.append({
                'id': detail['menu_item'],
                'name': MenuItem.objects.get(pk=detail['menu_item']).menu_item_name,
                'quantity': detail['sum']
            })
        return data


class OrdersYearAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {}
        datetime_format = '%Y-%m-%d'
        current_date = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        last_year_date = current_date - datetime.timedelta(days=365)
        while current_date >= last_year_date:
            data[current_date.strftime(datetime_format)] = 0
            current_date -= datetime.timedelta(days=1)
        orders = Order.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            start_datetime__gte=last_year_date
        ).values('start_datetime__date').annotate(sum=Count("id"))
        for order in orders:
            data[order['start_datetime__date'].strftime(datetime_format)] = order['sum']
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
