from django.urls import path

from .views import RegisterView, UserNameValidationView, EmailValidationView, VerificationView, LoginView, LogoutView, \
    RequestPasswordResetView, CompletePasswordResetView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "validate_username",
        csrf_exempt(UserNameValidationView.as_view()),
        name="validate_username",
    ),
    path(
        "validate-email",
        csrf_exempt(EmailValidationView.as_view()),
        name="validate_email",
    ),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('set-new-password/<uidb64>/<token>/', CompletePasswordResetView.as_view(), name='reset-user-password'),
    path('reset-password/',RequestPasswordResetView.as_view(),name='reset-password'),
]
