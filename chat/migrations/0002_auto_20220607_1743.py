# Generated by Django 2.2.6 on 2022-06-07 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Introduce',
            new_name='Room',
        ),
    ]
