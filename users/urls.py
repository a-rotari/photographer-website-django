from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path("login/", views.UserLoginView.as_view(next_page="/"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("password-reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset-sent/",
        PasswordResetDoneView.as_view(
            template_name="users/password_reset_done_override.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete"),
            template_name="users/password_reset_confirm_override.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete_override.html"
        ),
        name="password_reset_complete",
    ),
]
