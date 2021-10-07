from django.urls import path, include

from apps.provider.views import ListCreateProviderAPIView, RetrieveUpdateDestroyProviderAPIView

urlpatterns = [
    path('', ListCreateProviderAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyProviderAPIView.as_view())
]
