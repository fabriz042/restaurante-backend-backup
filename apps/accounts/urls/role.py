from django.urls import path

from apps.accounts.views import ListCreateRoleAPIView, RetrieveUpdateDestroyRoleAPIView

urlpatterns = [
    path('', ListCreateRoleAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyRoleAPIView.as_view()),
]