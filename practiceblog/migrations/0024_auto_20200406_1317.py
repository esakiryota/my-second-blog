# Generated by Django 2.2.6 on 2020-04-06 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0023_auto_20200406_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='cate',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科')], default='数学', max_length=200),
        ),
        migrations.AlterField(
            model_name='solve',
            name='user_name',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科')], default='数学', max_length=200),
        ),
    ]