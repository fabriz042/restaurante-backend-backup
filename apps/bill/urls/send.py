from django.urls import path

from apps.bill.views import BillOrderServiceAPIView

urlpatterns = [
    path('order/<pk>', BillOrderServiceAPIView.as_view()),
]
