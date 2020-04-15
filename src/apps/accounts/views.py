from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib import messages

from .decorators import anonymous_required
from .forms import SigninForm, SignupForm


class IndexView(TemplateView):

    auth_template_name = 'accounts/auth-index.html'
    anon_template_name = 'accounts/anon-index.html'

    def get_template_names(self):
        if self.request.user.is_anonymous:
            return [self.anon_template_name]
        return [self.auth_template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            context['signin_form'] = SigninForm()
            context['signup_form'] = SignupForm()
        return context


@method_decorator(anonymous_required, name='dispatch')
class SigninView(View):

    template_name = 'accounts/signin.html'
    form_class = SigninForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


@method_decorator(anonymous_required, name='dispatch')
class SignupView(View):

    template_name = 'accounts/signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
        return render(request, self.template_name, {'form': form})


class SignoutView(View):

    def get(self, request):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class SettingsView(TemplateView):

    template_name = 'accounts/settings.html'


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class CustomPasswordChangeView(View):

    template_name = 'accounts/change-password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, message='Password has been changed.')
            return redirect('password-change')
        return render(request, self.template_name, {'form': form})
