from django.apps import AppConfig


class BookingWebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_website'

    def ready(self):
        import booking_website.signals
