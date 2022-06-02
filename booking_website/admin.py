from django.contrib import admin
from django.utils.html import format_html
from booking_website.models import Booking, Restaurant, BookingFee, BookingReview, Table, RestaurantFees


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'table',)


@admin.register(BookingFee)
class BookingFeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount',)


@admin.register(BookingReview)
class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_text', 'restaurant', 'user',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    @admin.display(description='Image')
    def image_html(self, obj):
        return format_html(f'<img src="{obj.image_url}" width="100" />')

    list_display = ('name', 'description', 'image_html', 'subscription_fee_level')


@admin.register(RestaurantFees)
class RestaurantFeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount',)


@admin.register(Table)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'seats_number',)
