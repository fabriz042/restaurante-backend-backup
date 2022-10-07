import datetime
from io import BytesIO
from django_filters import rest_framework as filters
import pytz
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from xhtml2pdf import pisa
from apps.hall.models import Table
from apps.menu.models import MenuProduct, MenuRecipe
from apps.operations.filter import OrderFilter, PaymentDocumentFilter
from apps.operations.models import PaymentType, Purchase, PurchaseDetail, Order, OrderDetail, PaymentDocument, Serie, \
    ReturnedOrder
from apps.operations.serializers import PaymentTypeSerializer, PurchaseSerializer, PurchaseDetailSerializer, \
    OrderSerializer, OrderDetailSerializer, OrderExtendedSerializer, PaymentDocumentSerializer, SerieSerializer, OrderSunatSerializer, ReturnedOrderSerializer, ReturnedOrderSunatSerializer
from apps.warehouse.models import WarehouseMovement
from apps.warehouse.serializers import WarehouseMovementSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead
from shared.pagination import CustomPagination


class PaymentTypeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PaymentType.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PaymentTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PaymentType.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PurchaseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'payment_type', 'currency', 'provider'
    ]

    def get_queryset(self):
        return Purchase.objects.select_related(
            'payment_type', 'currency', 'provider', 'payment_document'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PurchaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Purchase.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PurchaseDetailListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PurchaseDetailSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'operation'
    ]

    def get_queryset(self):
        return PurchaseDetail.objects.select_related(
            'movement', 'movement__product'
        ).filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        movement_data = self.request.data
        movement_serializer = WarehouseMovementSerializer(data=movement_data)
        movement_serializer.is_valid(raise_exception=True)
        serializer.save(
            movement=movement_serializer.save(restaurant=self.request.user.profile.restaurant)
        )


class PurchaseDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseDetailSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PurchaseDetail.objects.select_related(
            'movement', 'movement__product'
        ).filter(
            is_active=True,
            operation__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        instance.movement.is_active = False
        instance.movement.save()

    def perform_update(self, serializer):
        movement_data = self.request.data
        movement_serializer = WarehouseMovementSerializer(
            instance=self.get_object().movement,
            data=movement_data
        )
        movement_serializer.is_valid(raise_exception=True)
        movement_serializer.save()
        serializer.save()


class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter',
        'client'
    ]

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        instance = serializer.save(restaurant=self.request.user.profile.restaurant)
        instance.table.state = Table.State.BUSSY
        instance.table.save()
        series = Serie.objects.filter(
            restaurant=instance.restaurant,
            code=instance.serie
        )
        for serie in series:
            serie.correlative += 1
            serie.save()


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        instance.table.state = Table.State.FREE
        instance.table.save()

        details = instance.details.filter(is_active=True)
        for detail in details:
            detail.is_active = False
            detail.save()
            recipe_menu = MenuRecipe.objects.filter(id=detail.menu_item.id)
            if len(recipe_menu) > 0:
                recipe_menu[0].daily_quantity += detail.quantity
                recipe_menu[0].save()
            detail.movements.all().update(is_active=False)

    def perform_update(self, serializer):
        self.get_object()
        serializer.save()


class OrderDetailListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'header'
    ]

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        data = serializer.validated_data
        menu_recipes = MenuRecipe.objects.filter(id=data['menu_item'].id)
        menu_products = MenuProduct.objects.filter(id=data['menu_item'].id)
        if len(menu_recipes) > 0:
            menu_recipe = menu_recipes[0]
            if menu_recipe.daily_quantity >= data['quantity']:
                menu_recipe.daily_quantity -= data['quantity']
                menu_recipe.save()
            else:
                raise ValidationError({'detail': 'No se tienen suficientes platos para consumir este plato'})
        if len(menu_products) > 0:
            product = menu_products[0].product
            stock = WarehouseMovement.objects.filter(is_active=True, product_id=product.id).aggregate(Sum('quantity'))['quantity__sum']
            stock = stock if stock else 0
            if stock >= data['quantity']:
                pass
            else:
                raise ValidationError({'detail': 'No se tienen suficientes productos para este pedido'})
        instance = serializer.save()
        instance.unit_price = instance.menu_item.sell_price
        instance.save()
        make_movements_per_detail(instance)  # stock discount


class OrderDetailRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        instance.movements.all().update(is_active=False)

        menu_recipes = MenuRecipe.objects.filter(id=instance.menu_item.id)
        if len(menu_recipes) > 0:
            menu_recipe = menu_recipes[0]
            menu_recipe.daily_quantity += instance.quantity
            menu_recipe.save()


class OrderDetailMakeMovementsAPIViews(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return OrderDetail.objects.filter(
            is_active=True,
            header__restaurant__user_profiles__user=self.request.user
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        is_product = MenuProduct.objects.filter(id=instance.menu_item.id)
        is_recipe = MenuRecipe.objects.filter(id=instance.menu_item.id)
        movements = []
        if len(is_product) > 0:
            movement = WarehouseMovement(
                restaurant=instance.header.restaurant,
                warehouse=instance.menu_item.warehouse,
                quantity=instance.quantity * -1,
                product=is_product[0].product
            )
            movement.save()
            instance.movements.add(movement)
            instance.save()
        if len(is_recipe) > 0:
            for recipe_detail in is_recipe[0].recipe.details.all():
                movement = WarehouseMovement(
                    restaurant=instance.header.restaurant,
                    warehouse=instance.menu_item.warehouse,
                    quantity=instance.quantity * recipe_detail.quantity * -1,
                    product=recipe_detail.product
                )
                movement.save()
                instance.movements.add(movement)
                instance.save()
                movements.append(movement)
        return Response(WarehouseMovementSerializer(movements, many=True).data)


class OpenedOrderListAPIView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderExtendedSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter'
    ]

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).prefetch_related('details').filter(
            end_datetime=None,
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )


class OrderExtendedListAPIView(generics.ListAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderExtendedSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'table',
        'waiter'
    ]

    def get_queryset(self):
        details_state = self.request.query_params.get('details__state', None)
        queryset = Order.objects.select_related(
            'table', 'waiter'
        ).prefetch_related('details').filter(
            # end_datetime=None,
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )
        if details_state:
            self.details_score = details_state.split(',')
            queryset = queryset.filter(details__state__in=details_state.split(',')).distinct().prefetch_related(
                'details')
        return queryset


class PurchaseTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [DjangoModelPermissionsWithRead]
    queryset = Purchase.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        purchase = self.get_object()
        html = render_to_string('ticket_purchase.html', {
            'purchase': purchase,
            'details': purchase.details.filter(is_active=True)
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Comprobante_{}-{}.pdf'.format(
            purchase.serie,
            str(purchase.correlative)
        )
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


class PaymentDocumentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentDocumentSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentDocumentFilter

    def get_queryset(self):
        return PaymentDocument.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class PaymentDocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentDocumentSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return PaymentDocument.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class OrderTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    class TicketType:
        IGV = 4
        NO_IGV = 2
        KITCHEN = 0

    # permission_classes = [DjangoModelPermissionsWithRead]
    ticket_type = TicketType.IGV
    queryset = Order.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        html = render_to_string('ticket_order.html', {
            'order': order,
            'details': order.details.filter(is_active=True),
            'ticket_type': self.ticket_type,
            'ticket_types': OrderTicketAPIView.TicketType()
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Comprobante_{}-{}.pdf'.format(
            order.serie,
            str(order.correlative)
        )
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


class SerieListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SerieSerializer
    permission_classes = [DjangoModelPermissionsWithRead]
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'payment_document'
    ]

    def get_queryset(self):
        return Serie.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            restaurant=self.request.user.profile.restaurant
        )


class SerieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SerieSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return Serie.objects.filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class OrderClosedListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = OrderSunatSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_class = OrderFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        query_page_size = int(self.request.query_params['page_size']) if 'page_size' in self.request.query_params else 0
        if query_page_size > 20:
            self.serializer_class = OrderSerializer
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            end_datetime__isnull=False
        ).order_by('-id')


class OrderTicketNoIGVAPIView(OrderTicketAPIView):
    ticket_type = OrderTicketAPIView.TicketType.NO_IGV


class OrderTicketKitchenAPIView(OrderTicketAPIView):
    ticket_type = OrderTicketAPIView.TicketType.KITCHEN


class AdditionalTicketAPIView(generics.UpdateAPIView):
    template_name = 'ticket_order.html'
    ticket_type = OrderTicketAPIView.TicketType.KITCHEN

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
        )

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        html = render_to_string(self.template_name, {
            'order': order,
            'details': order.details.filter(
                is_active=True,
                id__in=request.data
            ),
            'ticket_type': self.ticket_type,
            'ticket_types': OrderTicketAPIView.TicketType()
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Comprobante_{}-{}.pdf'.format(
            order.serie,
            str(order.correlative)
        )
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


class CloseOrderAPIView(generics.UpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseMovementSerializer

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            end_datetime__isnull=True
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        order.end_datetime = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        order.save()
        order.table.state = Table.State.FREE
        order.table.save()
        return Response(status=200)


def make_movements_per_detail(instance, positive=False):
    criteria = -1 if not positive else 1
    is_product = MenuProduct.objects.filter(id=instance.menu_item.id)
    is_recipe = MenuRecipe.objects.filter(id=instance.menu_item.id)
    movements = []
    if len(is_product) > 0:
        movement = WarehouseMovement(
            restaurant=instance.header.restaurant,
            warehouse=instance.menu_item.warehouse,
            quantity=instance.quantity * criteria,
            product=is_product[0].product
        )
        movement.save()
        instance.movements.add(movement)
        instance.save()
    if len(is_recipe) > 0:
        for recipe_detail in is_recipe[0].recipe.details.all():
            movement = WarehouseMovement(
                restaurant=instance.header.restaurant,
                warehouse=instance.menu_item.warehouse,
                quantity=instance.quantity * recipe_detail.quantity * criteria,
                product=recipe_detail.product
            )
            movement.save()
            instance.movements.add(movement)
            instance.save()
            movements.append(movement)
    return movements


class CloseAllOrderAPIView(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = WarehouseMovementSerializer

    def get_queryset(self):
        return Order.objects.select_related(
            'table', 'waiter'
        ).filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user,
            end_datetime__isnull=True
        )
    
    def create(self, request, *args, **kwargs):
        orders = self.get_queryset()
        # movements = []
        for order in orders:
            order.table.state = Table.State.FREE
            order.table.save()
        orders.update(end_datetime=datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))
        return Response(status=200)


class ReturnedOrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReturnedOrderSunatSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query_page_size = int(self.request.query_params['page_size']) if 'page_size' in self.request.query_params else 0
        if query_page_size > 20:
            self.serializer_class = ReturnedOrderSerializer
        return ReturnedOrder.objects.select_related(
            'related_order__table', 'related_order__waiter').filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        instance = serializer.save(
            restaurant=self.request.user.profile.restaurant
        )
        for detail in instance.related_order.details.all():
            make_movements_per_detail(detail, positive=True)


class ReturnedOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReturnedOrderSunatSerializer
    permission_classes = [DjangoModelPermissionsWithRead]

    def get_queryset(self):
        return ReturnedOrder.objects.select_related(
            'related_order__table', 'related_order__waiter').filter(
            is_active=True,
            restaurant__user_profiles__user=self.request.user
        ).order_by('-id')

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        for detail in instance.related_order.details.all():
            make_movements_per_detail(detail)
