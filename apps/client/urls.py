from django.urls import path

from apps.client.views import ListCreateClientAPIView, RetrieveEditDestroyClientAPIView

urlpatterns = [
    path('', ListCreateClientAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyClientAPIView.as_view())
]
