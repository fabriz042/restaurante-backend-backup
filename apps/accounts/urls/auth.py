from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from apps.accounts.views import RegisterUserAPIView, ListUserAuthPermissionsAPIView, RetrieveUpdateProfileAuthAPIView, \
    RetrieveUpdateUserAuthAPIView

urlpatterns = [
    path('', obtain_auth_token),
    path('register/', RegisterUserAPIView.as_view()),
    path('permissions/', ListUserAuthPermissionsAPIView.as_view()),
    path('user/', RetrieveUpdateUserAuthAPIView.as_view()),
    path('profile/', RetrieveUpdateProfileAuthAPIView.as_view())
]