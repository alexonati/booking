from django.contrib import admin
from django.utils.html import format_html
from booking_website.models import Booking, BookingFee, BookingReview


# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'table',)

    readonly_fields = ('booking_fee_level',)

    @admin.display(description='Booking Fee Level')
    def booking_fee_level(self, obj):
        return obj.booking_fee_level

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_id=request.user.id)

        return queryset


@admin.register(BookingFee)
class BookingFeeAdmin(admin.ModelAdmin):
    list_display = ('level', 'amount',)


@admin.register(BookingReview)
class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_text',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_id=request.user.id)

        return queryset
