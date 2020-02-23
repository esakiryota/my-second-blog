from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import Image
from .models import Question
from .models import Solve
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, FindForm, ImageForm, QuestionForm, SolveForm
from django.db.models import Q
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import requests

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
    solve = Solve.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
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
        api = "https://notify-api.line.me/api/notify"
        token = "RzQGOlPivhqQ8XTopvf7UqVIfwyb4lLqQzeCxjef5kf"
        headers = {"Authorization" : "Bearer "+ token}
        message = "\n[生徒情報]\n{0} {1} {2}\n[場所]\n{3}\n[曜日]\n{4}\n[開始時間]\n{5}\n[授業時間]\n{6}\n[希望性別]\n{7}\n[初回日程候補]\n{8} {9}\n{10} {11}\n{12} {13}\n[備考]\n{14}".format(name, grade, sex,place,  week, start_time, class_time, hope_sex, first_date1, first_time1, first_date2, first_time2 , first_date3,first_time3, something)
        payload = {"message" :  message}
        post = requests.post(api, headers = headers, params=payload)
        return render(request, 'practiceblog/post_list.html')
    return render(request, 'practiceblog/teacher_form.html')
