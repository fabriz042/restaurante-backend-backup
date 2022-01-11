from django.urls import path

from apps.bill.views import BillingSettingsRetrieveUpdateAPIView

urlpatterns = [
    path('', BillingSettingsRetrieveUpdateAPIView.as_view())
]
