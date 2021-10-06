from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.accounts.urls.auth')),
    path('user/', include('apps.accounts.urls.user')),
    path('role/', include('apps.accounts.urls.role')),
]