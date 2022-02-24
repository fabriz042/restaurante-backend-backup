from django.urls import path

from apps.accounts.views import ListCreateUserAPIView, RetrieveUpdateDestroyUserAPIView, WaiterUserListAPIView

urlpatterns = [
    path('', ListCreateUserAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyUserAPIView.as_view()),
    path('waiter/', WaiterUserListAPIView.as_view())
]