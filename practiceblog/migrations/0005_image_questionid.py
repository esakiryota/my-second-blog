# Generated by Django 2.2.6 on 2020-01-17 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0004_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='questionId',
            field=models.IntegerField(default=0),
        ),
    ]