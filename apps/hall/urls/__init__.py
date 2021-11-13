from django.urls import path, include

from apps.hall.views import HallListCreateAPIView, HallRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', HallListCreateAPIView.as_view()),
    path('<pk>', HallRetrieveUpdateDestroyAPIView.as_view()),
    path('table/', include('apps.hall.urls.table'))
]
