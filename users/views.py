from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordContextMixin
from django.views.generic import CreateView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from .models import User
from .helpers import send_email


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

    def check_if_user_exists(self, form_errors):
        key = 'email'
        value = 'User with this Email already exists.'
        if key in form_errors and value in form_errors[key]:
            if len(form_errors) == 1:
                return True
            else:
                del form_errors['email']
        return False

    def form_invalid(self, form):
        email = self.request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # User does not exist, proceed with validation results
            return super().form_invalid(form)
        else:
            if (not user.is_active) and (self.check_if_user_exists(form.errors)):
                form = CustomUserCreationForm(self.request.POST, instance=user)
                user = form.save()
                self.prepare_token_and_send_email(user)
                return HttpResponseRedirect(self.success_url)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Save user registration data as inactive
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.prepare_token_and_send_email(user)

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"text": "Home", "href": reverse("galleries:display_homepage")},
            {"text": "Registration", "href": "#"},
        ]
        return context

    def prepare_token_and_send_email(self, user):
        # Generate confirmation token
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Build confirmation link
        current_site = get_current_site(self.request)
        confirmation_url = reverse("users:user_activation", kwargs={"uidb64": uidb64, "token": token})
        confirmation_url = f"{self.request.scheme}://{current_site}{confirmation_url}"

        # Send confirmation email
        subject = "Confirm Your Registration"
        message = f"Click the following link to confirm your registration:\n\n{confirmation_url}"
        from_email = None
        recipient_list = [user.email]
        send_email(self.request, subject, message, from_email, recipient_list)


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
        return context


class UserActivationView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (ValueError, User.DoesNotExist):
            return HttpResponse("Invalid activation link.")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:login')  # Redirect to login page or any other page

        return HttpResponse("Invalid activation link.")


def delete_user(request):
    success = False

    breadcrumbs = [
                {'text': 'Home', 'href': reverse('galleries:display_homepage')},
                {'text': 'Client Area', 'href': reverse("galleries:client_area")},
            ]
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('galleries:client_area'))
        id = request.POST.get('id', '')
        user = User.objects.filter(id=id).first()
        if user == request.user:
            user.is_active = False
            user.save()
            logout(request)
            breadcrumbs.append({'text': 'User Deleted!', 'href': '#'})
            success = True
    else:
        breadcrumbs.append({'text': 'Delete User', 'href': '#'})
    return render(request,
                  'users/delete_user.html',
                  {'breadcrumbs': breadcrumbs,
                   'success': success}
                )
