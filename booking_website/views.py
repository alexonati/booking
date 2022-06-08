# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, HttpResponse
from booking_website.forms import RegisterForm, ProfileAvatarForm
from booking_website.models import Restaurant, Booking, BookingReview, Table


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
            return redirect(reverse('user_dashboard_view'))

    return render(request, 'register.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect(reverse('homepage'))


@login_required
def user_dashboard_view(request):
    if request.method == 'GET':
        form = ProfileAvatarForm()
    else:
        form = ProfileAvatarForm(files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('user_dashboard_view'))
    return render(request, 'dashboard.html', {
        'form': form})


def get_all_restaurants(request):
    restaurants = Restaurant.objects.all()
    tables = Table.objects.all()

    return render(request, 'dashboard.html', {
        'restaurants': restaurants,
        'tables': tables,
    })


def get_all_bookings(request):
    bookings = Booking.objects.all()

    return render(request, 'dashboard.html', {
        'bookings': bookings
    })


def get_all_reviews(request):
    reviews = BookingReview.objects.all()

    return render(request, 'dashboard.html', {
        'reviews': reviews
    })


def make_a_booking(request):
    return redirect(reverse('bookings'))


def make_a_review(request):
    return redirect(reverse('reviews'))


def delete_a_review(request):
    return redirect(reverse('reviews'))


def edit_a_review(request):
    return redirect(reverse('reviews'))
