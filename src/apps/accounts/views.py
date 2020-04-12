from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import anonymous_required


@method_decorator(anonymous_required, name='dispatch')
class SignInView(View):
    ''' User sign-in view. '''

    template_name = 'accounts/sign-in.html'
    form_class = AuthenticationForm

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
