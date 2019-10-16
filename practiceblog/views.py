from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, FindForm
from django.db.models import Q
from django.shortcuts import redirect
from django.core.paginator import Paginator

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
