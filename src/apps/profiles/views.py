from django.shortcuts import render
from django.views.generic.base import TemplateView


class ProfilePageView(TemplateView):

    template_name = 'profiles/profile.html'
