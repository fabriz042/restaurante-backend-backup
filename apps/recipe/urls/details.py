from django.urls import path

from apps.recipe.views import ListCreateRecipeDetailAPIView, RetrieveUpdateDestroyRecipeDetailAPIView

urlpatterns = [
    path('', ListCreateRecipeDetailAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyRecipeDetailAPIView.as_view())
]
