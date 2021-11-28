from django.urls import path, include

urlpatterns = [
    path('payment_type/', include('apps.operations.urls.payment_type')),
    path('purchase/', include('apps.operations.urls.purchase')),
    path('order/', include('apps.operations.urls.order')),
]
