from email.mime import image
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post, ProfileList, RoomList
from .models import Solve
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, FindForm, ImageBoxForm, QuestionForm, SolveForm, UserCreateForm, QuestionBoxForm, QuestionSolveForm, TeacherStudentForm, SolveForm
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
from django.http import HttpResponse
from django.shortcuts import render
import json
from datetime import date, datetime
from .serializer import UserSerializer, SolveSerializer
import django_filters
from rest_framework import viewsets
from django_filters import rest_framework as filters
# from django.utils import six 
from .repositories.userTokenListRepository import UserTokenListRepository
from .repositories.relationshipListRepository import RelationshipListRepository
from .repositories.userRepository import UserRepository
from .repositories.profileListRepository import ProfileListRepository
from .aws_s3_storage import MediaStorage
from django.contrib.auth import login

def index(request):
    return render(request, 'practiceblog/index.html')

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

@login_required
def profile(request, str="str", num=1):
    author = request.user.username
    rps = UserTokenListRepository()
    token = rps.getUserToken(request.user)
    prof_rps = ProfileListRepository()
    profile = prof_rps.getProfileByAuthor(request.user)
    image_src = ""
    if profile["image"] != "":
        image_src = prof_rps.getImageByUrl(profile["image"])
    params = {
    'author': author,
    'token': token,
    'profile': profile,
    'image_src' : image_src
    }
    return render(request, 'practiceblog/profile.html', params)

@login_required
def boardList(request,  num=1):
    user = request.user
    rps = UserTokenListRepository()
    token_list = rps.getTokenListByMutalFollow(user)
    params = {"token_list": token_list}
    print(params)
    return render(request, 'practiceblog/board_list.html', params)


def explanation(request):
    return render(request, 'practiceblog/explanation.html')

@login_required
def myboard(request, room_name):
    rps = UserTokenListRepository()
    user_token = rps.getUserToken(request.user)
    board_owner = rps.getUserInfoByToken(room_name)
    relation_rps = RelationshipListRepository()
    relation_bool = relation_rps.getRalationShipBool(board_owner.pk, request.user.pk)
    prf_rps = ProfileListRepository()
    profile = prf_rps.getProfileByAuthor(request.user)
    image_src = ""
    if profile["image"] != "":
        image_src = prf_rps.getImageByUrl(profile["image"])
    if relation_bool == False and user_token != room_name:
        return redirect("user_list")
    params = {"token": room_name, "user_name": user_token, "user": request.user.username, "image": image_src}
    return render(request, 'whiteboard/myboard.html', params)

@login_required
def rooms(request):
    data = RoomList.objects.order_by('created_date').reverse()
    return render(request, 'whiteboard/rooms.html',{
        'room_list' : data
    })

@login_required
def userList(request):
    usr_rps = UserRepository()
    # user_list = usr_rps.getUserAllListForView()
    author_id = request.user.pk
    relation_rps = RelationshipListRepository()
    relation_list = relation_rps.getRelationshipListByUserId(author_id)
    prf_rps = ProfileListRepository()
    user_list = prf_rps.getAllProfilesForView()
    params = {"user_list": user_list, "user_id": author_id, "relation_list": relation_list}
    return render(request, 'practiceblog/user_list.html', params)

@login_required
def room(request, room_name):
    data = RoomList.objects.order_by('created_date').reverse()
    print(data)
    return render(request, 'whiteboard/room.html', {
        'room_name': room_name,
        'room_list' : data
    })

User = get_user_model()


def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            prf_rps = ProfileListRepository()
            prf_rps.insert(user, user.username)
            return redirect('/')
    else:
        form = UserCreateForm()
    return render(request, 'register/user_create.html', {'form': form})

class UserCreate(generic.CreateView):
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self,request):
        user = form.save(commit=True)
        user.is_active = True
        user.save()

        # current_site = get_current_site(self.request)
        # domain = current_site.domain
        # context = {
        #     'protocol': self.request.scheme,
        #     'domain': domain,
        #     'token': dumps(user.pk),
        #     'user': user,
        # }

        # subject = render_to_string('register/mail_template/create/subject.txt', context)
        # subject = "家庭教師紹介-会員登録-"
        # message = render_to_string('register/mail_template/create/message.txt', context)

        # from_email = 'esaki1217@gmail.com'  # 送信者
        # recipient_list = [self.request.POST.get('email')]  # 宛先リスト
        # send_mail(subject, message, from_email, recipient_list)
        login(request, user)

        return render(request, '/')



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