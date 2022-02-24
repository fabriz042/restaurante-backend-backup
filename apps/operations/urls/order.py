from django.urls import path, include

from apps.operations.views import OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView, OpenedOrderListAPIView, \
    OrderExtendedListAPIView, OrderTicketAPIView, OrderClosedListCreateAPIView, OrderTicketNoIGVAPIView, \
    OrderTicketKitchenAPIView, AdditionalTicketAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view()),
    path('<pk>', OrderRetrieveUpdateDestroyAPIView.as_view()),
    path('opened/', OpenedOrderListAPIView.as_view()),
    path('extended/', OrderExtendedListAPIView.as_view()),
    path('detail/', include('apps.operations.urls.order_detail')),
    path('ticket/<pk>', OrderTicketAPIView.as_view()),
    path('ticket/no_igv/<pk>', OrderTicketNoIGVAPIView.as_view()),
    path('ticket/kitchen/<pk>', OrderTicketKitchenAPIView.as_view()),
    path('ticket/add/<pk>', AdditionalTicketAPIView.as_view()),
    path('closed/', OrderClosedListCreateAPIView.as_view()),
]
