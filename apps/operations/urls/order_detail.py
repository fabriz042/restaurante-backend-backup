from django.urls import path, include

from apps.operations.views import OrderDetailListCreateAPIView, OrderDetailRetrieveDestroyAPIView, \
    OrderDetailMakeMovementsAPIViews

urlpatterns = [
    path('', OrderDetailListCreateAPIView.as_view()),
    path('<pk>', OrderDetailRetrieveDestroyAPIView.as_view()),
    path('make_moves/<pk>', OrderDetailMakeMovementsAPIViews.as_view())
]