from django.urls import path

from apps.operations.views import PaymentTypeListCreateAPIView, PaymentTypeRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', PaymentTypeListCreateAPIView.as_view()),
    path('<pk>', PaymentTypeRetrieveUpdateDestroyAPIView.as_view())
]