from django.urls import path

from apps.accounts.views import RestaurantRetrieveUpdateAPIView, RestaurantPictureRetrieveUpdateAPIView

urlpatterns = [
    path('', RestaurantRetrieveUpdateAPIView.as_view()),
    path('picture/', RestaurantPictureRetrieveUpdateAPIView.as_view())
]