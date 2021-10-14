from django.urls import path

from apps.provider.views import ListCreatePrizingTableAPIView, RetrieveEditDestroyPrizingTableAPIView

urlpatterns = [
    path('', ListCreatePrizingTableAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyPrizingTableAPIView.as_view())
]