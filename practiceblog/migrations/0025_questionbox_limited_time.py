# Generated by Django 2.2.6 on 2020-08-10 14:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0024_auto_20200503_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbox',
            name='limited_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]