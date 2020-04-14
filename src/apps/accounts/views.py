from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView

from .decorators import anonymous_required
from .forms import LoginForm, SignupForm


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
            context['login_form'] = LoginForm()
            context['signup_form'] = SignupForm()
        return context


@method_decorator(anonymous_required, name='dispatch')
class LoginView(View):

    template_name = 'accounts/login.html'
    form_class = LoginForm

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


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
