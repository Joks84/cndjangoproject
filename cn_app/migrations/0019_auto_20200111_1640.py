# Generated by Django 3.0 on 2020-01-11 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cn_app', '0018_signup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
