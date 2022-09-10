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
    GRADE = (
        ('中学１年', '中学１年'),
        ('中学２年', '中学２年'),
        ('中学３年', '中学３年'),
        ('高校１年', '高校１年'),
        ('高校２年', '高校２年'),
        ('高校３年', '高校３年'),
    )
    NEW_OLD = (
        ('新規', '新規'),
        ('復習', '復習'),
    )
    INDI_PUB = (
        ('一般', '一般'),
        ('個人', '個人'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="タイトル")
    cate = models.CharField(max_length=200,choices=CATE,  default='数学')
    time = models.IntegerField(default=30)
    grade = models.CharField(max_length=200,choices=GRADE,  default='高校１年')
    new_old = models.CharField(max_length=200,choices=NEW_OLD,  default='新規')
    indi_pub = models.CharField(max_length=200,choices=INDI_PUB,  default='一般')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to = 'media/', default='some name')
    limited_time = models.DateTimeField(default=timezone.now)

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
    user_name = models.CharField(max_length=200)
    cate = models.CharField(max_length=200,choices=CATE, default='数学')
    questionId = models.IntegerField(default=0)
    score = models.IntegerField(default=100)
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

class TeacherStudent(models.Model):
    teacher_student = models.CharField(max_length=200, default='先生_生徒')
    user_teacher = models.IntegerField(default=0)
    user_student = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.teacher_student

class RoomList(models.Model):
    room_name = models.CharField(max_length=200, default='先生_生徒')
    url_token = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    participants = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.room_name
    
class UserTokenList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.token

class RelationshipList(models.Model):
    follow = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)

    def __str__(self):
        display = str(self.follow) + "->" + str(self.follower)
        return display