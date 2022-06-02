from django.contrib import admin
from django.urls import path

from booking_website.views import homepage, login_view, register_view, logout_view, profile_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

]
