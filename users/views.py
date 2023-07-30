from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def send_email(request):
    user = request.user
    subject = 'Test Subject'
    message = 'Test Message'
    user.email_user(subject, message)
    return redirect('display_homepage')
