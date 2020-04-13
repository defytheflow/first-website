from django.urls import path

from .views import SignInPage, SignUpPage, SignOutView

urlpatterns = [
    path('sign-in',  SignInPage.as_view(),  name='sign-in'),
    path('sign-up',  SignUpPage.as_view(),  name='sign-up'),
    path('sign-out', SignOutView.as_view(), name='sign-out'),
]
