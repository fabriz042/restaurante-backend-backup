from django.urls import path

from apps.hall.views import TableCreateAPIView, TableRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', TableCreateAPIView.as_view()),
    path('<pk>', TableRetrieveUpdateDestroyAPIView.as_view())
]
