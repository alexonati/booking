# Generated by Django 4.0.4 on 2022-07-03 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_website', '0007_alter_booking_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='QR_code',
        ),
    ]