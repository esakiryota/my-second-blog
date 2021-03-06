# Generated by Django 2.2.6 on 2020-03-20 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practiceblog', '0014_remove_questionbox_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSolve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('user_name', models.CharField(default='noname', max_length=200)),
                ('cate', models.CharField(default='some category', max_length=200)),
                ('questionId', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(default='some name', upload_to='media/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
