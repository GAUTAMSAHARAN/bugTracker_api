# Generated by Django 3.0.6 on 2020-05-16 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bugTracker', '0004_auto_20200516_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]