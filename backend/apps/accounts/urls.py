from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    ProfileView,
    PasswordChangeView,
    UserRegistrationView,
)


urlpatterns = [
    path('token/',LoginView.as_view(), name = 'token_pair'),
    path('token/refresh/',RefreshTokenView.as_view(), name = 'refresh_token'),
    path('token/revoke/',LogoutView.as_view(),name="remove_cookies"),

    path('register/',UserRegistrationView.as_view(),name="register"),
    path('me/',ProfileView.as_view(),name="user_profile"),

    path('me/password/',PasswordChangeView.as_view(),name="change_password"),
    # path('me/password-reset/',PasswordChangeView.as_view(),name="request_password_reset"),
    # path('me/password-confirm/',PasswordChangeView.as_view(),name="confirm_password_reset"),

    # path('verify-email/',VerifyEmailView.as_view(),name="verify_email"),
    # path('verify-phone/',VerifyPhoneView.as_view(),name="verify_phone"),
]