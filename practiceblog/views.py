from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Solve
from django.shortcuts import render, get_object_or_404
from .forms import SolveForm, UserCreateForm, SolveForm
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
from datetime import date, datetime
from .serializer import UserSerializer, SolveSerializer
import django_filters
from rest_framework import viewsets
from django_filters import rest_framework as filters
from django.utils import six 
from .repositories.userTokenListRepository import UserTokenListRepository

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def search_alg(arg):
    searchArg = {}
    for k, v in arg.items():
        if v[0] == "" or k == 'csrfmiddlewaretoken':
            continue
        searchArg[k] = v
    return searchArg

def profile(request, str="str", num=1):
    author = request.user.username
    data = Solve.objects.filter(user_name=author)
    cate = ""
    title = ""
    if (request.method == 'POST'):
        post_dict = dict(six.iterlists(request.POST))
        seach = search_alg(post_dict)
        request.session["form_value"] = seach
        for k, v in seach.items():
            if k == "cate":
                data = data.filter(cate__contains=v[0])
                cate = v[0]
            if k == "title":
                data = data.filter(title__contains=v[0])
                title = v[0]
    elif 'form_value' in request.session:
        seach = request.session['form_value']
        for k, v in seach.items():
            if k == "cate":
                data = data.filter(cate__contains=v[0])
                cate = v[0]
            if k == "title":
                data = data.filter(title__contains=v[0])
                title = v[0]
    else:
        data = Solve.objects.filter(user_name=author).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    data = data.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    tests = data.all()[:7].values_list("id","cate", "title", "score", "created_date")
    page = Paginator(tests, 3)
    test_list = page.get_page(num)
    math_list = []
    english_list = []
    for test in test_list:
        if test[1] == "数学":
            math_list.append(test)
        if test[1] == "英語":
            english_list.append(test)
    data_json_list_math  = json.dumps(math_list, default=json_serial)
    data_json_english  = json.dumps(english_list, default=json_serial)
    form = SolveForm(initial={"cate": cate, "title": title})
    rps = UserTokenListRepository()
    token = rps.getUserToken(request.user)
    params = {
    'author': author,
    'data': data,
    'data_json_math': data_json_list_math,
    'data_json_english': data_json_english,
    'tests': page.get_page(num),
    'form': form,
    'token': token,
    }
    return render(request, 'practiceblog/profile.html', params)

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

class CustomFilter(filters.FilterSet):
    start_created_date = filters.DateTimeFilter(field_name='created_date', lookup_expr='gt')
    end_created_date = filters.DateTimeFilter(field_name='created_date', lookup_expr='lt')
    class Meta:
        model = Solve
        fields = ['start_created_date', 'end_created_date'] #定義したフィルタを列挙

# class CustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'results': data
#         })
import rest_framework

class StandardResultsSetPagination(rest_framework.pagination.LimitOffsetPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SolveViewSet(viewsets.ModelViewSet):
    queryset = Solve.objects.all()
    serializer_class = SolveSerializer
    filter_fields = ('cate', 'title')
    filter_class = CustomFilter