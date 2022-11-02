from django.urls import path
from . import views
from .views import UserViewSet, SolveViewSet
from rest_framework import routers
from .api import apis

# app_name = 'study_room'

urlpatterns = [
    path('', views.index, name=''),
    path('explanation', views.explanation, name='explanation'),
    path('logout', views.logout_view, name='logout'),
    path('user_create/', views.user_create, name='user_create'),
    # path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    # path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('explanation', views.explanation, name='explanation'),
    path('profile', views.profile, name='profile'),
    path('profile/<int:num>/', views.profile, name='profile'),
    path('profile/api/update/', apis.profile_update),
    # 勉強部屋
    # path('rooms', views.rooms, name='rooms'),
    # path('rooms/<str:room_name>/', views.room, name='room'),
    path('myboard/<str:room_name>/', views.myboard, name='myboard'),
    path('myboard/api/user_info', apis.getUserInfo),
    path('rooms/api/<str:room_name>/update/',  apis.updateRoom, name='updateRoom'),
    path('rooms/api/<str:room_name>/load',  apis.loadRoom, name='loadRoom'),
    # ホワイトボードリスト
    path('board_list', views.boardList, name='board_list'),
    path('board_list/api/search', apis.board_search),
    # ユーザーリスト
    path('user_list', views.userList, name='user_list'),
    path('user_list/api/search', apis.user_search),
    path('user_list/api/follow', apis.user_follow),
    path('user_list/api/unfollow', apis.user_unfollow),
    # お問い合わせ
    path('contact', views.contact, name="contact"),
]

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'solves', SolveViewSet)
