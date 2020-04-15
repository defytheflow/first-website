from django.urls import path

from .views import (
    SigninView, SignupView, SignoutView, SettingsView, CustomPasswordChangeView
)

urlpatterns = [
    path('signin',   SigninView.as_view(),  name='signin'),
    path('signup',   SignupView.as_view(),  name='signup'),
    path('signout',  SignoutView.as_view(), name='signout'),

    path('settings', SettingsView.as_view(), name='settings'),
    path('password/change', CustomPasswordChangeView.as_view(), name='password-change'),
]
