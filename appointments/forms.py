from django import forms


class AppointmentRegistrationForm(forms.Form):
    required_css_class = 'required_asterisk'

    email = forms.EmailField(max_length=254)
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(label='Phone', required=False)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 1800}),
        required=False
    )

class AppointmentMessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 1800}),
        required=False
    )


class LoginAndAppointmentRegistrationForm(AppointmentRegistrationForm):
    selected_date = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(max_length=254, widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.HiddenInput())
    last_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    phone_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    message = forms.CharField(widget=forms.HiddenInput(), required=False)

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )
