from django.urls import path, include

from apps.currency.views import ListCreateCurrencyAPIView, RetrieveEditDestroyCurrencyAPIView

urlpatterns = [
    path('', ListCreateCurrencyAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyCurrencyAPIView.as_view())
]
