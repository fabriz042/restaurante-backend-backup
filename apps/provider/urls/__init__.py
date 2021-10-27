from django.urls import path, include

from apps.provider.views import ListCreateProviderAPIView, RetrieveUpdateDestroyProviderAPIView, AccountListAPIView, \
    PayProviderAPIView

urlpatterns = [
    path('', ListCreateProviderAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyProviderAPIView.as_view()),
    path('account/', AccountListAPIView.as_view()),
    path('pay/', PayProviderAPIView.as_view()),
    path('pricing/', include('apps.provider.urls.pricing')),
]
