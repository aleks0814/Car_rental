# Generated by Django 3.0.10 on 2022-06-07 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_auto_20220606_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rental',
            options={'permissions': [('rzym_view_rental', 'rzym rental view')]},
        ),
    ]