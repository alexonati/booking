from django.contrib import admin
from django.urls import path

from booking_website.views import homepage, login_view, register_view, logout_view, login_or_register_view, \
    get_all_restaurants, user_dashboard_view, get_all_bookings, get_all_reviews, edit_profile

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls, name='admin'),
    path('login_or_register/', login_or_register_view, name='login_or_register_view'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user_dashboard/', user_dashboard_view, name='user_dashboard_view'),
    path('profile/', edit_profile, name='profile'),
    path('restaurants/', get_all_restaurants, name='restaurants'),
    path('bookings/', get_all_bookings, name='bookings'),
    path('reviews/', get_all_reviews, name='reviews'),
]
