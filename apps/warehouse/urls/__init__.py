from django.urls import path

from apps.warehouse.views import ListCreateWarehouseAPIView, RetrieveEditDestroyWarehouseAPIView

urlpatterns = [
    path('', ListCreateWarehouseAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyWarehouseAPIView.as_view()),
]
