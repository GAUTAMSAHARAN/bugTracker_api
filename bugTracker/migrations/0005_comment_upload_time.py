# Generated by Django 3.0.6 on 2020-05-19 08:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bugTracker', '0004_issue_upload_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]