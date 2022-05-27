from django.conf import global_settings
from django.db import models


# Create your models here.
class Booking(models.Model):
    user_id = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField()
    table_id = models.ForeignKey("Table",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None,
                                 related_name='tables')
    participants = models.IntegerField()
    booking_fee_amount = models.ForeignKey("BookingFee", on_delete=models.SET_NULL,
                                           null=True,
                                           default=None,
                                           related_name='bookingfee')
    QR_code = models.ImageField()
    card_no = models.IntegerField()


class RestaurantFees(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()


class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    description = models.CharField(max_length=128, unique=True, null=False, blank=False)
    review_id = models.ForeignKey("BookingReview", on_delete=models.SET_NULL,
                                  null=True,
                                  default=None,
                                  related_name='reviews')
    owner_password = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_account_email = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurantemail')
    booking_id = models.ForeignKey(Booking, on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   related_name='reviews')
    logo = models.ImageField(upload_to='restaurants/', null=True, default=None)
    subscription_fee_level = models.ForeignKey(RestaurantFees,
                                               on_delete=models.CASCADE,
                                               null=True,
                                               default=None,
                                               related_name='subscription'
                                               )


class Table(models.Model):
    restaurant_id = models.ForeignKey(Restaurant,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      default=None,
                                      related_name='tables')
    seats_number = models.IntegerField()


class BookingFee(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()


class BookingReview(models.Model):
    user_id = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    booking_id = models.ForeignKey(Booking,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   related_name='bookings')

    restaurant_id = models.ForeignKey(Restaurant,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      default=None,
                                      related_name='restaurant')
