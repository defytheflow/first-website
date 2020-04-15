from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class SignupForm(auth.forms.UserCreationForm):

    email = forms.EmailField(max_length=255)
    full_name = forms.CharField(max_length=255)

    field_order = ('full_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)


class SigninForm(auth.forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)

    error_messages = {
        'invalid_login': 'Incorrect username or password',
    }


class UsernameChangeForm(forms.Form):

    new_username = forms.CharField(max_length=128)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError('User with that username already exists.')
        return new_username

    def save(self):
        new_username = self.cleaned_data.get('new_username')
        self.user.username = new_username
        self.user.save()
        return self.user


class PasswordChangeForm(auth.forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
