from django.contrib import admin
from django.urls import path

from booking_website.views import homepage, login_view, register_view, logout_view, login_or_register_view, \
    get_all_restaurants, get_all_bookings, get_all_reviews, user_dashboard_view, make_a_booking, make_a_review, delete_a_review, edit_a_review

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls, name='admin'),
    path('login_or_register/', login_or_register_view, name='login_or_register_view'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user_dashboard/', user_dashboard_view, name='user_dashboard_view'),
    path('restaurants/', get_all_restaurants, name='restaurants'),
    path('bookings/', get_all_bookings, name='bookings'),
    path('reviews/', get_all_reviews, name='reviews'),
    path('book/', make_a_booking, name='book'),
    path('review/', make_a_review, name='review'),
    path('review/', delete_a_review, name='delete_review'),
    path('review/', edit_a_review, name='edit_review'),
]
