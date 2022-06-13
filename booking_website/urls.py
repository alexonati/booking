from django.contrib import admin
from django.urls import path

from booking_website.views import homepage, login_view, register_view, logout_view, login_or_register_view, \
    get_all_restaurants, get_all_bookings, get_all_reviews, user_dashboard_view, make_a_reservation, make_a_review, \
    delete_review, edit_review, edit_reservation, delete_reservation

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
    path('reservation/<int:restaurant_id>/<int:table_id>/', make_a_reservation, name='reservation'),
    path('edit_reservation/<int:booking_id>/', edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:booking_id>/', delete_reservation, name='delete_reservation'),
    path('review/<int:booking_id>/', make_a_review, name='review'),
    path('edit_review/<int:booking_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:booking_id>/', delete_review, name='delete_review'),

]
