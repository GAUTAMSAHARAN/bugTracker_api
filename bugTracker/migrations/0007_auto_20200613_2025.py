# Generated by Django 3.0.6 on 2020-06-13 20:25

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('bugTracker', '0006_user_disable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='desc',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]
