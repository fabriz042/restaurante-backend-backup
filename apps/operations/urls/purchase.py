from django.urls import path, include

from apps.operations.views import PurchaseListCreateAPIView, PurchaseRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PurchaseListCreateAPIView.as_view()),
    path('<pk>', PurchaseRetrieveUpdateDestroyAPIView.as_view()),
    path('detail/', include('apps.operations.urls.purchase_detail')),
]