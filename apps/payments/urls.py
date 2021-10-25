from django.urls import path

from apps.payments.views import PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PaymentListCreateAPIView.as_view()),
    path('<pk>', PaymentRetrieveUpdateDestroyAPIView.as_view())
]
