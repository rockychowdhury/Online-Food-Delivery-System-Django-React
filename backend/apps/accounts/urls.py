from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    ProfileView,
    PasswordChangeView,
    UserRegistrationView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    RequestEmailVerificationView,
    VerifyEmailView,
    RequestPhoneVerificationView,
    VerifyPhoneView,
)


urlpatterns = [
    path('token/',LoginView.as_view(), name = 'token_pair'),
    path('token/refresh/',RefreshTokenView.as_view(), name = 'refresh_token'),
    path('token/revoke/',LogoutView.as_view(),name="remove_cookies"),

    path('register/',UserRegistrationView.as_view(),name="register"),
    path('me/',ProfileView.as_view(),name="user_profile"),

    path('me/password/',PasswordChangeView.as_view(),name="change_password"),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('verify-email/request/', RequestEmailVerificationView.as_view(), name='request_email_verification'),
    path('verify-email/confirm/', VerifyEmailView.as_view(), name='verify_email'),
    
    path('verify-phone/request/', RequestPhoneVerificationView.as_view(), name='request_phone_verification'),
    path('verify-phone/confirm/', VerifyPhoneView.as_view(), name='verify_phone'),
]