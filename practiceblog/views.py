from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import Image
from .models import Question
from .models import Solve
from .models import Introduce
from .models import QuestionBox
from .models import QuestionSolve
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, FindForm, ImageForm, QuestionForm, SolveForm, UserCreateForm, QuestionBoxForm, QuestionSolveForm
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

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def explanation(request):
    return render(request, 'practiceblog/explanation.html')

def question_box(request, num=1):
    question_box = QuestionBox.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(question_box, 3)
    return render(request, 'practiceblog/question_box.html', {"posts": page.get_page(num)})

def question_make(request):
    form = QuestionBoxForm()
    if (request.method == 'POST'):
        req_form = QuestionBoxForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        images.save()
        return redirect('question_box')
    return render(request, 'practiceblog/question_make.html', {'form': form})

def question_solve(request, pk):
    image = get_object_or_404(QuestionBox, pk=pk)
    form = QuestionSolveForm()
    params = {
    'form': form,
    'image': image,
    };
    if (request.method == 'POST'):
        req_form = QuestionSolveForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = pk
        images.save()
        return redirect('question_box')
    return render(request, 'practiceblog/question_solve.html',  params)

def question_answer(request, num=1):
    username = request.user
    question_answer = QuestionSolve.objects.filter(user_name=username).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(question_answer, 3)
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
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = pk
        images.save()
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
    page = Paginator(data, 3)
    params = {
    'form': form,
    'posts': page.get_page(num),
    }
    return render(request, 'practiceblog/post_list.html', params)


def category(request, num=1, str='cate'):
    data = Post.objects.filter(cate__contains=str).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 3)
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
    page = Paginator(data, 3)
    params = {
    'title': 'Hello',
    'form': form,
    'str': str,
    'posts': page.get_page(num),
    }
    return render(request, 'practiceblog/find.html', params)

def student(request, num=1):
    test = Question.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    solve = Solve.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(test, 3)
    params = {
    'tests': page.get_page(num),
    'solves': solve,
    }
    return render(request, 'practiceblog/student.html', params)

def result(request, num=1):
    author = request.user.username
    solve = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(solve, 3)
    return render(request, 'practiceblog/result.html', {"solves": page.get_page(num)})

def question(request):
    form = QuestionForm()
    if (request.method == 'POST'):
        api = "https://notify-api.line.me/api/notify"
        token = "7oLUU1AEdegSvF3nbU7LvTcCN4Rfdmo6Qo9JsTyNr9M"
        headers = {"Authorization" : "Bearer "+ token}
        message = '新しいテストを発行しました！url: http://esakiryota.pythonanywhere.com/student'
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        req_form = QuestionForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        images.save()
        return redirect('teacher')
    return render(request, 'practiceblog/question.html', {'form': form})

def teacher(request, num=1):
    data = Image.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    page = Paginator(data, 3)
    return render(request, 'practiceblog/teacher.html', {'posts': page.get_page(num)})

def test(request, pk):
    form = ImageForm()
    question = get_object_or_404(Question, pk=pk)
    params = {
    'form': form,
    'question': question,
    }
    if (request.method == 'POST'):
        api = "https://notify-api.line.me/api/notify"
        token = "7oLUU1AEdegSvF3nbU7LvTcCN4Rfdmo6Qo9JsTyNr9M"
        headers = {"Authorization" : "Bearer "+ token}
        message = 'テストをときました！url: http://esakiryota.pythonanywhere.com/teacher'
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        req_form = ImageForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.published_date = timezone.now()
        images.questionId = pk
        images.save()
        return redirect('student')

    return render(request, 'practiceblog/test.html',  params)

def answer(request, pk):
    image = get_object_or_404(Image, pk=pk)
    id = image.questionId
    question = get_object_or_404(Question, pk=id)
    form = SolveForm()
    params = {
    'form': form,
    'image': image,
    'question': question,
    };
    if (request.method == 'POST'):
        api = "https://notify-api.line.me/api/notify"
        token = "7oLUU1AEdegSvF3nbU7LvTcCN4Rfdmo6Qo9JsTyNr9M"
        headers = {"Authorization" : "Bearer "+ token}
        message = '採点しました！url: http://esakiryota.pythonanywhere.com/teacher'
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        req_form = SolveForm(request.POST, request.FILES)
        images = req_form.save(commit=False)
        images.author = request.user
        images.user_name = image.author.username
        images.published_date = timezone.now()
        images.questionId = id
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
    page = Paginator(data, 3)
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
