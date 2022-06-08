from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from booking_website.models import Profile

AuthUser = get_user_model()


class Command(BaseCommand):
    help = 'Create a profile for all users without one.'

    def handle(self, *args, **options):
        users_without_profile = AuthUser.objects.filter(profile=None).all()
        for user in users_without_profile:
            Profile.objects.create(user=user)
