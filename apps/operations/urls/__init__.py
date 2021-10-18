from django.urls import path, include

urlpatterns = [
    path('payment_type/', include('apps.operations.urls.payment_type')),
]
