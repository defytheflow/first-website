from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def anonymous_required(function=None, redirect_url=None):

    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda user: user.is_anonymous,
        redirect_field_name=None,
        login_url=redirect_url
    )

    return actual_decorator(function) if function else actual_decorator
