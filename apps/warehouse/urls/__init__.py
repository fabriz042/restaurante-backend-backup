from django.urls import path, include

from apps.warehouse.views import ListCreateWarehouseAPIView, RetrieveEditDestroyWarehouseAPIView

urlpatterns = [
    path('', ListCreateWarehouseAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyWarehouseAPIView.as_view()),
    path('movement/', include('apps.warehouse.urls.movement')),
]
