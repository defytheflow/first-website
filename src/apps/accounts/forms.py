from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=255)
    full_name = forms.CharField(max_length=255)

    field_order = ('full_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.fields['username'].widget.attrs.pop("autofocus", None)


class SignInForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.fields['username'].widget.attrs.pop("autofocus", None)

    error_messages = {
        'invalid_login': 'Incorrect username or password',
    }
