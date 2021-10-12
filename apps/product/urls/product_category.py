from django.urls import path, include

from apps.product.views import ListCreateProductCategoryAPIView, PerformUpdateDestroyProductCategoryAPIView

urlpatterns = [
    path('', ListCreateProductCategoryAPIView.as_view()),
    path('<pk>', PerformUpdateDestroyProductCategoryAPIView.as_view())
]
