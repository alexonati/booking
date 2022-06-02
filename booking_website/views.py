# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, HttpResponse
from booking_website.forms import RegisterForm


def homepage(request):
    return render(request, 'landing_page.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('profile'))

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('profile'))

    return render(request, 'register.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect(reverse('homepage'))


@login_required
def profile_view(request):
    return HttpResponse('This is the profile route.')
