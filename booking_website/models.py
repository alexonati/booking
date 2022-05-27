from django.conf import global_settings
from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField()
    booking_id = models.ForeignKey("BookingReview",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   related_name='bookings')
    user_account_email = models.CharField()
    user_password = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField()
    card_no = models.IntegerField(max_length=16)


class Booking(models.Model):
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

    user_id = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True,
                                default=None,
                                related_name='users')
    QR_code = models.ImageField()
    card_no = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True,
                                default=None,
                                related_name='cardno')


class Restaurant(models.Model):
    name = models.CharField()
    description = models.CharField()
    review_id = models.ForeignKey("BookingReview", on_delete=models.SET_NULL,
                                  null=True,
                                  default=None,
                                  related_name='reviews')
    owner_password = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_account_email = models.CharField()
    booking_id = models.ForeignKey(Booking, on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   related_name='reviews')
    logo_image = models.ImageField()
    subscription_fee_amount = models.IntegerField()


class RestaurantFees(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()


class Table(models.Model):
    restaurant_id = models.ForeignKey(Restaurant,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      default=None,
                                      related_name='restaurant')
    seats_number = models.IntegerField()


class BookingFee(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()


class BookingReview(models.Model):
    user_id = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                default=None,
                                related_name='user')

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
