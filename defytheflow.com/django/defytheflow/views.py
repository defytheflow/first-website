from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect


def home_page(request):
    template_name = 'home_page.html'
    return render(request, template_name, {})


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/sport/')
        else:
            return render(request, '404.html')
    template_name = 'registration/login.html'
    return render(request, template_name, {})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
