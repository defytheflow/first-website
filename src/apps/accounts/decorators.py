from django.shortcuts import redirect


def anonymous_required(function):
    ''' Redirects authenticated user home. '''

    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)

    return decorator
