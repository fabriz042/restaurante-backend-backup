from django.urls import path

from apps.operations.views import OrderListCreateAPIView, OrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view()),
    path('<pk>', OrderRetrieveUpdateDestroyAPIView.as_view())
]