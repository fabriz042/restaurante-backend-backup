from django.urls import path, include

urlpatterns = [
    path('category/', include('apps.menu.urls.category')),
    path('product/', include('apps.menu.urls.product')),
    path('recipe/', include('apps.menu.urls.recipe'))
]
