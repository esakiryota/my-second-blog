# Generated by Django 2.2.6 on 2019-10-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cate',
            field=models.CharField(default='some category', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='some name', upload_to='media/'),
        ),
    ]