# Generated by Django 4.0.4 on 2022-06-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_website', '0002_remove_booking_review_bookingreview_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='review',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='BookingReview',
        ),
    ]
