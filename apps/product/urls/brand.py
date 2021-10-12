from django.urls import path, include

from apps.product.views import ListCreateBrandAPIView, PerformUpdateDestroyBrandAPIView

urlpatterns = [
    path('', ListCreateBrandAPIView.as_view()),
    path('<pk>', PerformUpdateDestroyBrandAPIView.as_view())
]
