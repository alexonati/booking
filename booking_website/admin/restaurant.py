from django.contrib import admin
from django.utils.html import format_html
from booking_website.models import Restaurant, Table, RestaurantFees


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    @admin.display(description='Image')
    def image_html(self, obj):
        return format_html(f'<img src="{obj.image_url}" width="100" />')

    @admin.display(description='Total bookings')
    def bookings_number(self, obj):
        return obj.bookings.count()

    readonly_fields = ('subscription_fee_level',)

    @admin.display(description='Subscription Fee Level')
    def subscription_fee_level(self, obj):
        return obj.subscription

    list_display = ('name', 'description', 'image_html', 'subscription_fee_level',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_owner=request.user)

        return queryset


@admin.register(RestaurantFees)
class RestaurantFeesAdmin(admin.ModelAdmin):
    list_display = ('level', 'amount',)


@admin.register(Table)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'seats_number',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_id=request.user.id)

        return queryset
