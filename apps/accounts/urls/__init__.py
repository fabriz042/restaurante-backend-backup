from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls.auth')),
    path('user/', include('apps.accounts.urls.user')),
    path('role/', include('apps.accounts.urls.role')),
    path('permission/', include('apps.accounts.urls.permission')),
    path('restaurant/', include('apps.accounts.urls.restaurant')),
]
