# Generated by Django 2.2.6 on 2020-04-06 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0024_auto_20200406_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(default='タイトル', max_length=200),
        ),
        migrations.AlterField(
            model_name='solve',
            name='title',
            field=models.CharField(default='タイトル', max_length=200),
        ),
    ]
