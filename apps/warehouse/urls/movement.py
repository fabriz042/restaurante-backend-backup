from django.urls import path

from apps.warehouse.views import ListCreateWarehouseMovementAPIView, RetrieveEditDestroyWarehouseMovementAPIView

urlpatterns = [
    path('', ListCreateWarehouseMovementAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyWarehouseMovementAPIView.as_view()),
]