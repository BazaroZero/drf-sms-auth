from django.urls import path

from .views import (
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    RegistrationAPIView,
)

urlpatterns = [
    path("users/", RegistrationAPIView.as_view(), name="registration"),
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]
