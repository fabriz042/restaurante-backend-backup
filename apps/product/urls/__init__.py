from django.urls import path, include

from apps.product.views import ListCreateProductAPIView, PerformUpdateDestroyProductAPIView

urlpatterns = [
    path('', ListCreateProductAPIView.as_view()),
    path('<pk>', PerformUpdateDestroyProductAPIView.as_view()),
    path('brand/', include('apps.product.urls.brand')),
    path('category/', include('apps.product.urls.product_category')),
    path('measurement_unit/', include('apps.product.urls.measurement_unit')),
]
