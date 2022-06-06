# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, HttpResponse
from booking_website.forms import RegisterForm
from booking_website.models import Restaurant, Booking, BookingReview


def homepage(request):
    return render(request, 'landing_page.html')


def login_or_register_view(request):
    return render(request, 'login_or_register_view.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(reverse('admin:index'))
            return redirect(reverse('user_dashboard_view'))

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_staff:
                return redirect(reverse('admin:index'))
            return redirect(reverse('profile'))

    return render(request, 'register.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect(reverse('homepage'))


@login_required
def user_dashboard_view(request):
    return render(request, 'user_dashboard.html')


def edit_profile(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_staff:
                return redirect(reverse('admin:index'))
            return redirect(reverse('profile'))

    return render(request, 'user_dashboard.html', {
        'form': form
    })


def get_all_restaurants(request):
    restaurants = Restaurant.objects.all()

    return render(request, 'user_dashboard.html', {
        'restaurants': restaurants
    })


def get_all_bookings(request):
    bookings = Booking.objects.all()

    return render(request, 'user_dashboard.html', {
        'bookings': bookings
    })


def get_all_reviews(request):
    reviews = BookingReview.objects.all()

    return render(request, 'user_dashboard.html', {
        'reviews': reviews
    })
