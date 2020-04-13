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

class ImageBox(models.Model):
    CATE = (
        ('数学', '数学'),
        ('英語', '英語'),
        ('理科', '理科'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="タイトル")
    cate = models.CharField(max_length=200, choices=CATE, default="科目")
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
    CATE = (
        ('数学', '数学'),
        ('英語', '英語'),
        ('理科', '理科'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="タイトル")
    cate = models.CharField(max_length=200,choices=CATE,  default='数学')
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
    CATE = (
        ('数学', '数学'),
        ('英語', '英語'),
        ('理科', '理科'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="タイトル")
    user_name = models.CharField(max_length=200,choices=CATE, default='数学')
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

class QuestionBox(models.Model):
    CATE = (
        ('数学', '数学'),
        ('英語', '英語'),
        ('理科', '理科'),
        ('その他', 'その他'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='タイトル')
    user_name = models.CharField(max_length=200, default='noname')
    cate = models.CharField(max_length=200,choices=CATE, default='数学')
    comment = models.CharField(max_length=300, default='ここにコメントがかかれます')
    bool = models.BooleanField(verbose_name='',default=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class QuestionSolve(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='タイトル')
    user_name = models.CharField(max_length=200, default='noname')
    cate = models.CharField(max_length=200, default='some category')
    comment = models.CharField(max_length=300, default='ここにコメントをお願いします。')
    bool = models.BooleanField(verbose_name='',default=False)
    questionId = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
