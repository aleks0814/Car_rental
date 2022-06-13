# Generated by Django 3.0.10 on 2022-06-09 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewer', '0018_auto_20220608_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='picture',
            field=models.ImageField(default=False, null=True, upload_to='viewer/picture'),
        ),
        migrations.CreateModel(
            name='ClientTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('complete', models.BooleanField(default=None)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['complete'],
            },
        ),
    ]