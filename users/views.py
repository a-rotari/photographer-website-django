from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordContextMixin
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"text": "Home", "href": reverse("galleries:display_homepage")},
            {"text": "Log In", "href": "#"},
        ]
        return context


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"text": "Home", "href": reverse("galleries:display_homepage")},
            {"text": "Registration", "href": "#"},
        ]
        return context


class UserPasswordResetView(PasswordResetView):
    success_url=reverse_lazy("users:password_reset_done")
    email_template_name="users/password_reset_email_override.html"
    template_name="users/password_reset_form_override.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"text": "Home", "href": reverse("galleries:display_homepage")},
            {"text": "Log In", "href": reverse("users:login")},
            {"text": "Reset Password", "href": "#"}
        ]
        print('hey')
        return context


def send_email(request):
    user = request.user
    subject = "Test Subject"
    message = "Test Message"
    user.email_user(subject, message)
    return redirect("display_homepage")
