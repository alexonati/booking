# Generated by Django 4.0.4 on 2022-07-03 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_website', '0009_booking_qr_code_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='QR_code_image',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
