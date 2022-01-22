from django.urls import path

from apps.stats.views import TopProductsAPIView, TopRecipesAPIView, OrdersYearAPIView

urlpatterns = [
    path('top/products/', TopProductsAPIView.as_view()),
    path('top/recipes/', TopRecipesAPIView.as_view()),
    path('order_year/', OrdersYearAPIView.as_view())
]
