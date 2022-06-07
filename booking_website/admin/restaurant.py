from django.contrib import admin
from django.utils.html import format_html
from booking_website.models import Restaurant, Table, RestaurantFees


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_html', 'restaurant_website_link', 'subscription_fee_level',)
    readonly_fields = ('subscription_fee_level',)

    @admin.display(description='Image')
    def image_html(self, obj):
        return format_html(f'<img src="{obj.image_url}" width="100" />')

    @admin.display(description='Total bookings')
    def bookings_number(self, obj):
        return obj.bookings.count()

    @admin.display(description='Subscription Fee Level')
    def subscription_fee_level(self, obj):
        return obj.subscription

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_owner=request.user)

        return queryset

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)

        if not request.user.is_superuser:
            fields.remove('restaurant_owner')
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and obj.pk is None:
            obj.restaurant_owner_id = request.user.id

        super().save_model(request, obj, form, change)


@admin.register(RestaurantFees)
class RestaurantFeesAdmin(admin.ModelAdmin):
    list_display = ('level', 'amount')

    def get_list_display(self, request):
        list_display = super().get_list_display(request)

        if not request.user.is_superuser:
            list_display = list(list_display)
            list_display.remove('amount')
        return list_display

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)

        if not request.user.is_superuser:
            fields.remove('amount')

        return fields


@admin.register(Table)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'seats_number',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(restaurant_id=request.user.id)

        return queryset
