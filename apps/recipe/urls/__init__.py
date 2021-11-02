from django.urls import path, include

from apps.recipe.views import ListCreateRecipeAPIView, RetrieveUpdateDestroyRecipeAPIView

urlpatterns = [
    path('', ListCreateRecipeAPIView.as_view()),
    path('<pk>', RetrieveUpdateDestroyRecipeAPIView.as_view()),
    path('detail/', include('apps.recipe.urls.details')),
]
