from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    # home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # admin
    path('admin/', admin.site.urls),
    # accounts
    path('', include('accounts.urls')),
    # profiles
    path('<slug:username>', include('profiles.urls')),
]
