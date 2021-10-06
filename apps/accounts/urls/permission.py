from django.urls import path

from apps.accounts.views import ListPermissionAPIView

urlpatterns = [
    path('', ListPermissionAPIView.as_view()),
]