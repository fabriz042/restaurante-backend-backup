from django.urls import path

from apps.operations.views import PaymentDocumentListCreateAPIView, PaymentDocumentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PaymentDocumentListCreateAPIView.as_view()),
    path('<pk>', PaymentDocumentRetrieveUpdateDestroyAPIView.as_view())
]