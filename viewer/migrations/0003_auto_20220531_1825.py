# Generated by Django 3.0.10 on 2022-05-31 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_auto_20220531_1844'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarClient',
            new_name='Booking',
        ),
    ]