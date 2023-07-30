from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model
from django.forms import CharField


class CustomUserCreationForm(BaseUserCreationForm):
    first_name = CharField(max_length=150, required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
