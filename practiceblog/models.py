from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cate = models.CharField(max_length=200, default='some category')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Image(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cate = models.CharField(max_length=200, default='some category')
    questionId = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cate = models.CharField(max_length=200, default='some category')
    time = models.IntegerField(default=30)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Solve(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200, default='esakiryota')
    cate = models.CharField(max_length=200, default='some category')
    questionId = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Introduce(models.Model):
    name = models.CharField(max_length=200, default='匿名')
    grade = models.CharField(max_length=200)
    place = models.CharField(max_length=200, default='some place')
    hope_sex = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    intro = models.BooleanField(verbose_name='',default=False)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
