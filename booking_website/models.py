from django.conf import global_settings
from django.db import models
from django.templatetags.static import static


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField()
    table = models.ForeignKey("Table",
                              on_delete=models.SET_NULL,
                              null=True,
                              default=None,
                              blank=True,
                              related_name='tables')
    participants = models.IntegerField()
    booking_fee_amount = models.ForeignKey("BookingFee", on_delete=models.SET_NULL,
                                           null=True,
                                           default=None,
                                           blank=True,
                                           related_name='bookingfee')
    QR_code = models.ImageField()
    card_no = models.IntegerField()

    def __str__(self):
        return f'"Booking" ({self.id})'


class RestaurantFees(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return f'"RestaurantFee" ({self.level})'


class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    description = models.CharField(max_length=128, unique=True, null=False, blank=False)
    owner_password = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_account_email = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                                 related_name='restaurantemail')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL,
                                null=True,
                                default=None,
                                blank=True,
                                related_name='bookings')
    image = models.ImageField(upload_to='booking_website/', null=True, default=None)
    subscription_fee_level = models.ForeignKey(RestaurantFees,
                                               on_delete=models.CASCADE,
                                               null=True,
                                               default=None,
                                               blank=True,
                                               related_name='subscription'
                                               )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static('..\static\images\defaultProductImage.png')

    def __str__(self):
        return f'{self.name} ({self.id})'


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   blank=True,
                                   related_name='tables')
    seats_number = models.IntegerField()

    def __str__(self):
        return f'"Table" ({self.id})'


class BookingFee(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return f'"BookingFee" ({self.level})'


class BookingReview(models.Model):
    user = models.ForeignKey(global_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    booking = models.ForeignKey(Booking,
                                on_delete=models.SET_NULL,
                                null=True,
                                default=None,
                                blank=True,
                                related_name='reviews')

    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   blank=True,
                                   related_name='restaurant')

    def __str__(self):
        return f'"BookingReview" ({self.id})'
