# Generated by Django 3.0.14 on 2022-09-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0034_profilelist_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelist',
            name='image',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
