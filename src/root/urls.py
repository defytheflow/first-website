from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.decorators import anonymous_required


urlpatterns = [
    path('',
        anonymous_required(
            TemplateView.as_view(template_name='index.html')
        ),
        name='index',
    ),
    path('home',
        login_required(
            TemplateView.as_view(template_name='home.html'),
            redirect_field_name=None,
        ),
        name='home',
    ),
    path('admin/', admin.site.urls),
    # accounts
    path('', include('accounts.urls')),
    # profiles
    path('<slug:username>', include('profiles.urls')),
]
