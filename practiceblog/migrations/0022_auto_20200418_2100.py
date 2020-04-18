# Generated by Django 2.2.6 on 2020-04-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practiceblog', '0021_auto_20200402_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagebox',
            name='cate',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科')], default='科目', max_length=200),
        ),
        migrations.AlterField(
            model_name='imagebox',
            name='title',
            field=models.CharField(default='タイトル', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='cate',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科')], default='数学', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(default='タイトル', max_length=200),
        ),
        migrations.AlterField(
            model_name='questionbox',
            name='cate',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科'), ('その他', 'その他')], default='数学', max_length=200),
        ),
        migrations.AlterField(
            model_name='questionsolve',
            name='cate',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科'), ('その他', 'その他')], default='数学', max_length=200),
        ),
        migrations.AlterField(
            model_name='solve',
            name='title',
            field=models.CharField(default='タイトル', max_length=200),
        ),
        migrations.AlterField(
            model_name='solve',
            name='user_name',
            field=models.CharField(choices=[('数学', '数学'), ('英語', '英語'), ('理科', '理科')], default='数学', max_length=200),
        ),
    ]
