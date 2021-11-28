from django.urls import path, include

from apps.operations.views import OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view()),
    path('<pk>', OrderRetrieveUpdateDestroyAPIView.as_view()),
    path('detail/', include('apps.operations.urls.order_detail')),
]