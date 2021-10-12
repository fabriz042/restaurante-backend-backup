from django.urls import path, include

urlpatterns = [
    path('brand/', include('apps.product.urls.brand')),
]
