from django.urls import path

from apps.menu.views import MenuRecipeListCreateAPIView, MenuRecipeRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MenuRecipeListCreateAPIView.as_view()),
    path('<pk>', MenuRecipeRetrieveUpdateDestroyAPIView.as_view())
]