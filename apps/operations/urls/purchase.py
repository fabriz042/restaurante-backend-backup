from django.urls import path

from apps.operations.views import PurchaseListCreateAPIView, PurchaseRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PurchaseListCreateAPIView.as_view()),
    path('<pk>', PurchaseRetrieveUpdateDestroyAPIView.as_view())
]