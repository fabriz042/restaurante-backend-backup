from django.urls import path

from apps.menu.views import MenuCategoryListCreateAPIView, MenuCategoryRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MenuCategoryListCreateAPIView.as_view()),
    path('<pk>', MenuCategoryRetrieveUpdateDestroyAPIView.as_view())
]