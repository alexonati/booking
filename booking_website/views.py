# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from booking_website.forms import RegisterForm, ProfileAvatarForm, MakeBookingForm
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


def restaurants_and_tables(request):
    restaurants = Restaurant.objects.all()
    tables = Table.objects.all()

    return {'restaurants': restaurants,
            'tables': tables}


def make_a_reservation(request, restaurant_id, table_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    table = get_object_or_404(Table, id=table_id)

    if request.method == 'GET':
        form = MakeBookingForm(request, user=request.user, restaurant=restaurant, table=table)
    else:
        form = MakeBookingForm(request.POST, user=request.user, restaurant=restaurant, table=table)

        # **** USED FOR DEBUG ****
        print('form.is_valid()', form.is_valid())
        for field in form:
            print("*****", field.name, field.errors, field.value())

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

        form = MakeBookingForm(request.POST, user=booking.user, restaurant=booking.restaurant, table=booking.table, instance=booking)
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


def make_a_review(request):
    return redirect(reverse('reviews'))


def delete_a_review(request):
    return redirect(reverse('reviews'))


def edit_a_review(request):
    return redirect(reverse('reviews'))
