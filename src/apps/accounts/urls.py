from django.urls import path

from .views import (
    SigninView, SignupView, SignoutView, SettingsView,
    UsernameChangeView, PasswordChangeView
)

urlpatterns = [
    path('signin',   SigninView.as_view(),  name='signin'),
    path('signup',   SignupView.as_view(),  name='signup'),
    path('signout',  SignoutView.as_view(), name='signout'),

    path('settings', SettingsView.as_view(), name='settings'),
    path('settings/username', UsernameChangeView.as_view(), name='username-change'),
    path('settings/password', PasswordChangeView.as_view(), name='password-change'),
]
