# Generated by Django 2.2.6 on 2022-09-07 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practiceblog', '0031_roomlist_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow', models.IntegerField(default=0)),
                ('follower', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserTokenList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
