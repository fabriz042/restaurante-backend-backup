from django.urls import path, include

urlpatterns = [
    path('brand/', include('apps.product.urls.brand')),
    path('category/', include('apps.product.urls.product_category')),
]
