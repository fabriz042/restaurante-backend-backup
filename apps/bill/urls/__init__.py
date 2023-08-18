from django.urls import path, include

from apps.bill.views import BillingSettingsRetrieveUpdateAPIView, BillingSettingsCertificateAPIView, BillRetrieveAPIView

urlpatterns = [
    path('', BillingSettingsRetrieveUpdateAPIView.as_view()),
    path('certificate/', BillingSettingsCertificateAPIView.as_view()),
    path('send/', include('apps.bill.urls.send')),
    path('info/<int:pk>', BillRetrieveAPIView.as_view())
]
