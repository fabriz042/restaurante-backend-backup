from django.urls import path, include

from apps.product.views import ListCreateMeasurementUnitAPIView, PerformUpdateDestroyMeasurementUnitAPIView

urlpatterns = [
    path('', ListCreateMeasurementUnitAPIView.as_view()),
    path('<pk>', PerformUpdateDestroyMeasurementUnitAPIView.as_view())
]
