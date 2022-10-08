import django_filters
from django_filters.rest_framework import FilterSet

from apps.operations.models import Order, PaymentDocument, ReturnedOrder


class OrderFilter(FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    start_date = django_filters.DateFilter(field_name='start_datetime__date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='start_datetime__date', lookup_expr='lte')

    class Meta:
        model = Order
        fields = [
            'table',
            'waiter',
            'client',
            'currency',
            'payment_type',
            'payment_document'
        ]


class PaymentDocumentFilter(FilterSet):

    class Meta:
        model = PaymentDocument
        fields = [
            'cancel_sale',
            'require_serie',
            'is_cancelable',
        ]


class ReturnedOrderFilter(FilterSet):
    start_date = django_filters.DateFilter(field_name='datetime__date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='datetime__date', lookup_expr='lte')

    class Meta:
        model = ReturnedOrder
        fields = [
            'related_order',
            'payment_document'
        ]
