from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfilePageView(TemplateView):

    template_name = 'profiles/profile.html'
