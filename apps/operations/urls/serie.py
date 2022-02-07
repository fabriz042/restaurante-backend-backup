from django.urls import path

from apps.operations.views import SerieListCreateAPIView, SerieRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', SerieListCreateAPIView.as_view()),
    path('<pk>', SerieRetrieveUpdateDestroyAPIView.as_view())
]
