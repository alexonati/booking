from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from booking_website.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(instance, **kwargs):
    print(f'*** POST_SAVE SIGNAL CALLED FOR {instance}')
    if not hasattr(instance, 'profile'):
        print(f'*** Create profile for {instance}.')
        Profile.objects.create(user=instance)
