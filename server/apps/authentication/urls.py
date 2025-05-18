from django.urls import path
from .views import (
    UserProfileView,
    LogoutView,
    UserRegistrationView,
    UserProfileUpdateView,
    PasswordChangeView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView
)

urlpatterns = [
    path('',UserProfileView.as_view(),name="user_profile"),
    path('token/',CustomTokenObtainPairView.as_view(), name = 'access_token'),
    path('token/refresh/',CustomTokenRefreshView.as_view(), name = 'refresh_token'),
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('token/verify/',CustomTokenVerifyView.as_view(), name = 'token_verify'),
    path('update-profile/',UserProfileUpdateView.as_view(),name="update_profile"),
    path('token/refresh/logout/',LogoutView.as_view(),name="logout"),
    path('change-password/',PasswordChangeView.as_view(),name="change_password"),
]