from django.urls import path

from apps.menu.views import MenuProductListCreateAPIView, MenuProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', MenuProductListCreateAPIView.as_view()),
    path('<pk>', MenuProductRetrieveUpdateDestroyAPIView.as_view())
]