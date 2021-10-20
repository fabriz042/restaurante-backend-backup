from django.urls import path, include

from apps.operations.views import PurchaseDetailListCreateAPIView, PurchaseDetailRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PurchaseDetailListCreateAPIView.as_view()),
    path('<pk>', PurchaseDetailRetrieveUpdateDestroyAPIView.as_view())
]
