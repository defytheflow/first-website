from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import anonymous_required
from .forms import SignUpForm, SignInForm


@method_decorator(anonymous_required, name='dispatch')
class SignUpView(View):

    template_name = 'accounts/sign-up.html'
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('sign-in')
        return render(request, self.template_name, {'form': form})


@method_decorator(anonymous_required, name='dispatch')
class SignInView(View):

    template_name = 'accounts/sign-in.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class SignOutView(View):

    def get(self, request):
        logout(request)
        return redirect('sign-in')
