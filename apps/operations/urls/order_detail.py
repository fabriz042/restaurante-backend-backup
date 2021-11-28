from django.urls import path, include

from apps.operations.views import OrderDetailListCreateAPIView, OrderDetailRetrieveDestroyAPIView

urlpatterns = [
    path('', OrderDetailListCreateAPIView.as_view()),
    path('<pk>', OrderDetailRetrieveDestroyAPIView.as_view()),
]