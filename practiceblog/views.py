from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import ImageBox
from .models import Question
from .models import Solve
from .models import Introduce
from .models import QuestionBox
from .models import QuestionSolve
from .models import TeacherStudent
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, FindForm, ImageBoxForm, QuestionForm, SolveForm, UserCreateForm, QuestionBoxForm, QuestionSolveForm, TeacherStudentForm
from django.db.models import Q
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views import generic
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import logout
import requests
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from django.http import HttpResponse
from django.shortcuts import render
import json

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def profile(request):
    author = request.user.username
    data = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    data_json_math = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).filter(cate__contains="数学").order_by('published_date').reverse().all()[:7].values_list("cate", "title", "score")
    data_json_english = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).filter(cate__contains="英語").order_by('published_date').reverse().all()[:7].values_list("cate", "title", "score")
    data_json_list_math = list(data_json_math)
    data_json_english = list(data_json_english)
    data_json_list_math  = json.dumps(data_json_list_math)
    data_json_english  = json.dumps(data_json_english)
    params = {
    'author': author,
    'data': data,
    'data_json_math': data_json_list_math,
    'data_json_english': data_json_english,
    }
    return render(request, 'practiceblog/profile.html', params)

def connect(request):
    teachers = User.objects.filter(groups__name='先生')
    user_pk = request.user.pk
    my_teachers_list = TeacherStudent.objects.filter(user_student=user_pk)
    return render(request, 'practiceblog/connect.html', {"teachers": teachers})

def connectOn(request, pk):
    req_form = TeacherStudentForm()
    user_pk = request.user.pk
    
    images = req_form.save(commit=False)
    images.user_teacher = pk
    images.user_student = request.user.pk
    images.teacher_student = pk + '_' + request.user.pk
    images.published_date = timezone.now()
    images.save()
    return redirect('profile')


def explanation(request):
    return render(request, 'practiceblog/explanation.html')

def question_box(request, num=1):
    question_box = QuestionBox.objects.filter(bool=False).filter(user_name="noname").filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(question_box, 10)
    return render(request, 'practiceblog/question_box.html', {"posts": page.get_page(num)})

def question_box_indiv(request, num=1):
    user_name = request.user
    question_box = QuestionBox.objects.filter(bool=False).filter(user_name=user_name).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(question_box, 10)
    return render(request, 'practiceblog/question_box.html', {"posts": page.get_page(num)})

def question_make(request):
    form = QuestionBoxForm()
    if (request.method == 'POST'):
        category = request.POST.get('subject')
        req_form = QuestionBoxForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        im = Image.open(images.image)
        orientation = get_exif_of_image(images.image).get('Orientation', 1)
        exif = get_exif_of_image(images.image)
        print(orientation)
        print(exif)
        print(images.image.path)
        api = "https://notify-api.line.me/api/notify"
        #テストtoken
        token = "rP3uTpG8LSuWANK1Dw9CSmU9Ss8TSGimvhANTM7i5Hh"
        headers = {"Authorization" : "Bearer "+ token}
        message = "質問がきました"
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        images.save()
        image_orientation_transpose(images.image.path)
        return redirect('question_box')
    return render(request, 'practiceblog/question_make.html', {'form': form})

def question_solve(request, pk):
    image = get_object_or_404(QuestionBox, pk=pk)
    form = QuestionSolveForm()
    image_file = image.image
    orientation = get_exif_of_image(image.image).get('Orientation', 1)
    params = {
    'form': form,
    'image': image,
    'orientation': orientation,
    };
    exif = get_exif_of_image(image.image)
    print(exif)
    # sys.exit()
    if (request.method == 'POST'):
        req_form = QuestionSolveForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = pk
        images.save()
        image_orientation_transpose(images.image.path)
        subject = "質問箱"
        message = "回答が返ってきました！\nhttp://esakiryota.pythonanywhere.com/question_answer"
        from_email = 'esaki1217@gmail.com'
        recipient_list = [image.author.email]
        send_mail(subject, message, from_email, recipient_list)
        image.bool = True
        image.save()
        return redirect('question_box')
    return render(request, 'practiceblog/question_solve.html',  params)

def question_answer(request, num=1):
    username = request.user
    question_answer = QuestionSolve.objects.filter(bool=False).filter(user_name=username).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(question_answer, 10)
    return render(request, 'practiceblog/question_answer.html', {"posts": page.get_page(num)})

def question_look(request, pk):
    image = get_object_or_404(QuestionSolve, pk=pk)
    form = QuestionBoxForm()
    params = {
    'form': form,
    'image': image,
    };
    if (request.method == 'POST'):
        req_form = QuestionBoxForm(request.POST, request.FILES)
        bool = request.POST.get('bool')
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = pk
        if (bool):
            images.bool = True
        images.save()
        if (bool != 'True'):
            image_orientation_transpose(images.image.path)
        subject = "質問箱"
        message = "個人への質問がきました！\nhttp://esakiryota.pythonanywhere.com/question_box_indiv"
        from_email = 'esaki1217@gmail.com'
        recipient_list = [image.author.email]
        send_mail(subject, message, from_email, recipient_list)
        image.bool = True
        image.save()
        return redirect('question_box')
    return render(request, 'practiceblog/question_look.html',  params)

def post_list(request, num=1):
    if (request.method == 'POST'):
        form = FindForm(request.POST)
        str = request.POST['find']
        val = str.split()
        data = Post.objects.filter(Q(cate__contains=str)|Q(title__contains=str)).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    else:
        form = FindForm()
        data = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 10)
    params = {
    'form': form,
    'posts': page.get_page(num),
    }
    return render(request, 'practiceblog/post_list.html', params)


def category(request, num=1, str='cate'):
    data = Post.objects.filter(cate__contains=str).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 10)
    params = {
    'str': str,
    'posts': page.get_page(num),
    }
    return render(request, 'practiceblog/category.html', params)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'practiceblog/post_detail.html', {'post': post})

def post_new(request):
    form = PostForm()
    return render(request, 'practiceblog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'practiceblog/post_edit.html', {'form': form})

def find(request, num=1, str='cate'):
    if (request.method == 'POST'):
        form = FindForm(request.POST)
        str = request.POST['find']
        val = str.split()
        data = Post.objects.filter(Q(title__contains=str)|Q(cate__contains=str)).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        return redirect('find', str=str, num=1)
    else:
        form = FindForm()
        data = Post.objects.filter(Q(title__contains=str)|Q(cate__contains=str)).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 10)
    params = {
    'title': 'Hello',
    'form': form,
    'str': str,
    'posts': page.get_page(num),
    }
    return render(request, 'practiceblog/find.html', params)

def student(request, num=1):
    form = QuestionForm()
    test = Question.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(test, 10)
    params = {
    'tests': page.get_page(num),
    'form': form,
    }
    return render(request, 'practiceblog/student.html', params)

def find_test(request, num=1, str="高校１年_新規_一般_"):
    if (request.method == 'POST'):
        search = request.POST.get('find')
        grade = request.POST.get('grade')
        new_old = request.POST.get('new_old')
        indi_pub = request.POST.get('indi_pub')
        str = grade + '_' + new_old + '_' + indi_pub + '_' + search
        return redirect('find_test', str=str, num=1)
    else:
        array_str = str.split('_')
        grade = array_str[0]
        new_old = array_str[1]
        indi_pub = array_str[2]
        search = array_str[3]
        if (len(search)):
            data = Question.objects.filter(Q(title__contains=search)|Q(title__contains=search)).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        else:
            data = Question.objects.filter(Q(grade__contains=grade)&Q(new_old__contains=new_old)&Q(indi_pub__contains=indi_pub)).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    form = QuestionForm()
    page = Paginator(data, 10)
    params = {
    'tests': page.get_page(num),
    'form': form,
    'str': str,
    }
    return render(request, 'practiceblog/find_test.html', params)


def result(request, num=1):
    author = request.user.username
    solve = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(solve, 10)
    return render(request, 'practiceblog/result.html', {"solves": page.get_page(num)})

def question(request):
    form = QuestionForm()
    if (request.method == 'POST'):
        # api = "https://notify-api.line.me/api/notify"
        # token = "7oLUU1AEdegSvF3nbU7LvTcCN4Rfdmo6Qo9JsTyNr9M"
        # headers = {"Authorization" : "Bearer "+ token}
        # message = '新しいテストを発行しました！url: http://esakiryota.pythonanywhere.com/student'
        # payload = {"message" :  message}
        # post = requests.post(api, headers = headers, params=payload)
        req_form = QuestionForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        images.save()
        return redirect('teacher')
    return render(request, 'practiceblog/question.html', {'form': form})

def teacher(request, num=1):
    data = ImageBox.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 10)
    return render(request, 'practiceblog/teacher.html', {'posts': page.get_page(num)})

def test(request, pk):
    form = ImageBoxForm()
    question = get_object_or_404(Question, pk=pk)
    nowtime = timezone.now()
    str_elasped_time = 0
    limited_time_zone = question.limited_time
    question_title = question.title + '_' + request.user.username
    question_cate = question.cate
    test_conductor = True
    time_loss = nowtime-limited_time_zone
    if (question.limited_time > nowtime) :
        elasped_time = question.limited_time-nowtime
        str_elasped_time = elasped_time.seconds
    elif ( time_loss.seconds > 60*60 ):
        test_conductor = False
    else :
        str_elasped_time = 5;
    params = {
    'form': form,
    'question': question,
    'elasped_time': str_elasped_time,
    'nowtime': nowtime,
    'limited_time_zone': limited_time_zone,
    'test_conductor': test_conductor,
    'question_title': question_title,
    'question_cate': question_cate,
    }
    if (request.method == 'POST'):
        # api = "https://notify-api.line.me/api/notify"
        #家庭教師token
        # token = "n8KpP4gWh2mkRbnVObxope3sVjCq5ldlTU4KYOeCDV5"
        #テストtoken
        # token = "rP3uTpG8LSuWANK1Dw9CSmU9Ss8TSGimvhANTM7i5Hh"
        # headers = {"Authorization" : "Bearer "+ token}
        # message = 'テストをときました！url: http://esakiryota.pythonanywhere.com/teacher'
        # payload = {"message" :  message}
        # post = requests.post(api, headers = headers, params=payload)
        req_form = ImageBoxForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        images.questionId = pk
        images.title = request.POST.get('title')
        images.cate = request.POST.get('cate')
        images.save()
        image_orientation_transpose(images.image.path)
        return redirect('student')

    return render(request, 'practiceblog/test.html',  params)

def answer(request, pk):
    image = get_object_or_404(ImageBox, pk=pk)
    id = image.questionId
    image_title = image.title + '_採点後'
    image_cate = image.cate
    id = image.questionId
    question = get_object_or_404(Question, pk=id)
    form = SolveForm()
    params = {
    'form': form,
    'image': image,
    'question': question,
    'image_title': image_title,
    'image_cate': image_cate,
    };
    if (request.method == 'POST'):
        # api = "https://notify-api.line.me/api/notify"
        #家庭教師token
        # token = "n8KpP4gWh2mkRbnVObxope3sVjCq5ldlTU4KYOeCDV5"
        #テストtoken
        # token = "rP3uTpG8LSuWANK1Dw9CSmU9Ss8TSGimvhANTM7i5Hh"
        # headers = {"Authorization" : "Bearer "+ token}
        # message = '採点しました！url: http://esakiryota.pythonanywhere.com/teacher'
        # payload = {"message" :  message}
        # post = requests.post(api, headers = headers, params=payload)
        req_form = SolveForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = id
        images.title = request.POST.get("title")
        images.cate = request.POST.get("cate")
        images.save()
        return redirect('teacher')
    return render(request, 'practiceblog/answer.html',  params)

def solve(request, pk):
    image = get_object_or_404(Solve, pk=pk)
    id = image.questionId
    question = get_object_or_404(Question, pk=id)
    params = {
    'image': image,
    'question': question,
    }
    return render(request, 'practiceblog/solve.html',  params)

def introduce(request):
    if (request.method == 'POST'):
        name = request.POST.get('name')
        grade = request.POST.get('grade')
        sex = request.POST.get('sex')
        place = request.POST.get('place')
        weekarray = request.POST.getlist('week')
        week = ""
        for w in weekarray:
            week += " " + w
        start_time = request.POST.get('start_time')
        class_time = request.POST.get('class_time')
        hope_sex = request.POST.get('hope_sex')
        first_date1 = request.POST.get('first_date1')
        first_time1 = request.POST.get('first_time1')
        first_date2 = request.POST.get('first_date2')
        first_time2 = request.POST.get('first_time2')
        first_date3 = request.POST.get('first_date3')
        first_time3 = request.POST.get('first_time3')
        something = request.POST.get('something')

        intro = Introduce(name=name, grade=grade, place=place, hope_sex=hope_sex, )
        intro.save()

        api = "https://notify-api.line.me/api/notify"
        #家庭教師token
        # token = "n8KpP4gWh2mkRbnVObxope3sVjCq5ldlTU4KYOeCDV5"
        #テストtoken
        token = "rP3uTpG8LSuWANK1Dw9CSmU9Ss8TSGimvhANTM7i5Hh"
        headers = {"Authorization" : "Bearer "+ token}
        message = "\n[生徒情報]\n{0} {1} {2}\n[場所]\n{3}\n[曜日]\n{4}\n[開始時間]\n{5}\n[授業時間]\n{6}\n[希望性別]\n{7}\n[初回日程候補]\n{8} {9}\n{10} {11}\n{12} {13}\n[備考]\n{14}".format(name, grade, sex,place,  week, start_time, class_time, hope_sex, first_date1, first_time1, first_date2, first_time2 , first_date3,first_time3, something)
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        return render(request, 'practiceblog/post_list.html')
    return render(request, 'practiceblog/teacher_form.html')

def teacherIntroduce(request, num=1):
    data = Introduce.objects.filter(intro=False).order_by('created_date').reverse()
    page = Paginator(data, 10)
    if (request.method == 'POST'):
        pk = request.POST.get('intro_id')
        user_name = request.user.username
        intro_model = Introduce.objects.get(pk=pk)
        intro_name = intro_model.name
        intro_model.intro = True
        intro_model.save()
        api = "https://notify-api.line.me/api/notify"
        #家庭教師token
        # token = "n8KpP4gWh2mkRbnVObxope3sVjCq5ldlTU4KYOeCDV5"
        #テストtoken
        token = "rP3uTpG8LSuWANK1Dw9CSmU9Ss8TSGimvhANTM7i5Hh"
        headers = {"Authorization" : "Bearer "+ token}
        message = "{0} が {1}の案件を応募しました。".format(user_name, intro_name)
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        return render(request, 'practiceblog/introduce.html', {'posts': page.get_page(num)})
    return render(request, 'practiceblog/introduce.html', {'posts': page.get_page(num)})

User = get_user_model()

class UserCreate(generic.CreateView):
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self,form):
        user = form.save(commit=True)
        user.is_active = False
        group = self.request.POST.get('groups')
        user.groups.add(group)
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        # subject = render_to_string('register/mail_template/create/subject.txt', context)
        subject = "家庭教師紹介-会員登録-"
        message = render_to_string('register/mail_template/create/message.txt', context)

        from_email = 'esaki1217@gmail.com'  # 送信者
        recipient_list = [self.request.POST.get('email')]  # 宛先リスト
        send_mail(subject, message, from_email, recipient_list)



        return redirect('user_create_done')

class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'
#
class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

def get_exif_of_image(file):
    im = Image.open(file)
    try:
        exif = im._getexif()
    except AttributeError:
        return {}

    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する

    exif_table = {}

    try:
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_table[tag] = value
    except AttributeError:
        return exif_table
    return exif_table

def image_orientation_transpose(file):
    im = Image.open(file)
    orientation = get_exif_of_image(file).get('Orientation', 1)
    if orientation == 6:
        im = im.transpose(Image.ROTATE_270)
    # return im
    im.save(file)
