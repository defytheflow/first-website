from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings

from .decorators import anonymous_required
from .forms import SignupForm, LoginForm


@method_decorator(anonymous_required, name='dispatch')
class LoginPage(View):

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
class SignupPage(View):

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
        return redirect(settings.LOGIN_URL)
