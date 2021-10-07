from django.urls import path, include

from apps.document_type.views import ListCreateDocumentTypeAPIView, RetrieveEditDestroyDocumentTypeAPIView

urlpatterns = [
    path('', ListCreateDocumentTypeAPIView.as_view()),
    path('<pk>', RetrieveEditDestroyDocumentTypeAPIView.as_view())
]
