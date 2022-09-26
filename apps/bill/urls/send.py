from django.urls import path

from apps.bill.views import BillOrderServiceAPIView, BillReturnedOrderServiceAPIView

urlpatterns = [
    path('order/<pk>', BillOrderServiceAPIView.as_view()),
    path('devolution/<pk>', BillReturnedOrderServiceAPIView.as_view()),
]
