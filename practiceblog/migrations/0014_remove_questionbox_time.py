# Generated by Django 2.2.6 on 2020-03-20 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0013_questionbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionbox',
            name='time',
        ),
    ]