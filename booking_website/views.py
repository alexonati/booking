# Create your views here.
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from booking_website.forms import RegisterForm, ProfileAvatarForm, MakeBookingForm
from booking_website.models import Restaurant, Booking, Table


def homepage(request):
    return render(request, 'landing_page.html')


def login_or_register_view(request):
    # check if user.is_authenticated & if yes, redirect to user_dashboard.html
    # if not, render the below page
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
        else:
            messages.warning(request, 'Username or password is incorrect. Please retry.')
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

    tables_paginator = Paginator(tables, 5)
    tables_page_obj = request.GET.get('page', 1)
    tables_page = tables_paginator.get_page(tables_page_obj)

    return render(request, 'dashboard.html', {
        'tables_page': tables_page,
        'restaurants': restaurants,
    })


def get_all_bookings(request):
    bookings = Booking.objects.all()

    bookings_paginator = Paginator(bookings, 5)
    bookings_page_obj = request.GET.get('page', 1)
    bookings_page = bookings_paginator.get_page(bookings_page_obj)

    return render(request, 'dashboard.html', {

        'bookings_page' : bookings_page
    })


def get_all_reviews(request):
    bookings = Booking.objects.all()
    restaurants = Restaurant.objects.all()

    reviews_paginator = Paginator(bookings, 5)
    reviews_page_obj = request.GET.get('page', 1)
    reviews_page = reviews_paginator.get_page(reviews_page_obj)

    return render(request, 'dashboard.html', {
        'reviews_page': reviews_page,
        'bookings': bookings,
    })


def restaurants_and_tables(request):
    restaurants = Restaurant.objects.all()
    tables = Table.objects.all()

    return {'restaurants': restaurants,
            'tables': tables}


def make_a_reservation(request, restaurant_id, table_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    table = get_object_or_404(Table, id=table_id)

    if request.method == 'GET':
        form = MakeBookingForm(user=request.user, restaurant=restaurant, table=table)
    else:
        form = MakeBookingForm(request.POST, user=request.user, restaurant=restaurant, table=table)

        # # **** USED FOR DEBUG ****
        # print('form.is_valid()', form.is_valid())
        # for field in form:
        #     print("*****", field.name, field.errors, field.value())

        if form.is_valid():
            form.save()
            table.booked = True
            table.save()

            return redirect(reverse('bookings'))

    return render(request, 'make_reservation_page.html', {
        'form': form})


def edit_reservation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    form = MakeBookingForm(user=booking.user, restaurant=booking.restaurant, table=booking.table, instance=booking)

    if request.method == 'POST':

        form = MakeBookingForm(request.POST, user=booking.user, restaurant=booking.restaurant,
                               table=booking.table, instance=booking)

        print('form.is_valid()', form.is_valid())
        for field in form:
            print("*****", field.name, field.errors, field.value())

        if form.is_valid():
            form.save()
            return redirect(reverse('bookings'))

    return render(request, 'make_reservation_page.html', {
        'form': form})


def delete_reservation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    table = get_object_or_404(Table, id=booking.table.pk)

    if request.method == 'POST':
        booking.delete()
        table.booked = False
        table.save()
        return redirect(reverse('bookings'))

    return render(request, 'delete_booking.html', {
        'booking': booking})


def make_a_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.review = request.POST.get('content')
        booking.save()
        return redirect(reverse('reviews'))

    return render(request, 'make_review_page.html', {
        'booking': booking})


def edit_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.review = request.POST.get('content')
        booking.save()
        return redirect(reverse('reviews'))

    return render(request, 'make_review_page.html', {
        'booking': booking})


def delete_review(request, booking_id):
    Booking.objects.filter(id=booking_id).update(review=None)

    return redirect(reverse('bookings'))
