from django.conf import global_settings, settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, BaseValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=None, blank=False, null=False)
    time = models.TimeField(default=None, blank=False, null=False)
    review = models.TextField(default=None, blank=True, null=True)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   blank=True,
                                   related_name='booking_restaurant')
    table = models.ForeignKey("Table",
                              on_delete=models.SET_NULL,
                              null=True,
                              default=None,
                              blank=True,
                              related_name='table')
    booking_fee_level = models.ForeignKey("BookingFee", on_delete=models.SET_NULL,
                                          null=True,
                                          default=1,
                                          blank=True,
                                          related_name='bookingfee')
    QR_code_image = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return f'Booking {self.id}'


class RestaurantFees(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.level}'


class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    description = models.CharField(max_length=128, unique=True, null=False, blank=False)
    restaurant_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='booking_website/restaurant_logo', null=True, blank=True, default=None)
    restaurant_website_link = models.URLField(null=True,
                                              default=None,
                                              blank=True)
    subscription_fee_level = models.ForeignKey(RestaurantFees,
                                               on_delete=models.CASCADE,
                                               null=True,
                                               default=1,
                                               blank=True,
                                               related_name='subscription'
                                               )

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static('..\static\images\defaultProductImage.png')

    def __str__(self):
        return f'{self.name}'


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=None,
                                   blank=True,
                                   related_name='tables')
    seats_number = models.PositiveIntegerField(null=False, default=1,
                                               validators=[MaxValueValidator(20), MinValueValidator(1)])
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'


class BookingFee(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.level}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='booking_website/user_avatars', null=True, blank=True, default=None)

    @property
    def image_url(self):
        if self.avatar:
            return self.avatar.url
        return static('..\static\images\defaultUserAvatar.jpg')


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **kwargs):

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(first_name, last_name, email, password, **kwargs)


class AuthUser(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=150, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=False)
    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
