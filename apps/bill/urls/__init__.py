from django.urls import path

from apps.bill.views import BillingSettingsRetrieveUpdateAPIView, BillingSettingsCertificateAPIView

urlpatterns = [
    path('', BillingSettingsRetrieveUpdateAPIView.as_view()),
    path('certificate/', BillingSettingsCertificateAPIView.as_view())
]
