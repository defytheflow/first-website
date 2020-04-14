from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home',
        login_required(
            TemplateView.as_view(template_name='home.html'),
            redirect_field_name=None,
        ),
        name='home',
    ),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
]
