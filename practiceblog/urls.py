from django.urls import path
from . import views
<<<<<<< HEAD
from .views import UserViewSet, SolveViewSet
from rest_framework import routers
=======
from .api import apis
>>>>>>> socket_chat

# app_name = 'study_room'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('find/<str>/<int:num>/', views.find, name='find'),
    path('logout', views.logout_view, name='logout'),
    path('find/', views.find, name='find'),
    path('category/', views.category, name='category'),
    path('category/<str>', views.category, name='category'),
    path('category/<str>/<int:num>/', views.category, name='category'),
    path('<int:num>', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('student', views.student, name='student'),
    path('student/<int:num>/', views.student, name='student'),
    path('find_test/', views.find_test, name='find_test'),
    path('find_test/<str>/<int:num>/', views.find_test, name='find_test'),
    path('result', views.result, name='result'),
    path('result/<int:num>/', views.result, name='result'),
    path('teacher', views.teacher, name='teacher'),
    path('teacher/<int:num>/', views.teacher, name='teacher'),
    path('test', views.test, name='test'),
    path('test/<int:pk>/', views.test, name='test'),
    path('answer', views.answer, name='answer'),
    path('answer/<int:pk>/', views.answer, name='answer'),
    path('question', views.question, name='question'),
    path('solve/<int:pk>', views.solve, name='solve'),
    path('introduce', views.introduce, name='introduce'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('introduce_all', views.teacherIntroduce, name='introduce_all'),
    path('introduce_all/<int:num>/', views.teacherIntroduce, name='introduce_all'),
    path('explanation', views.explanation, name='explanation'),
    path('question_box', views.question_box, name='question_box'),
    path('question_box/<int:num>/', views.question_box, name='question_box'),
    path('question_box_indiv', views.question_box_indiv, name='question_box_indiv'),
    path('question_box_indiv/<int:num>/', views.question_box_indiv, name='question_box_indiv'),
    path('question_make', views.question_make, name='question_make'),
    path('question_solve', views.question_solve, name='question_solve'),
    path('question_solve/<int:pk>/', views.question_solve, name='question_solve'),
    path('question_answer', views.question_answer, name='question_answer'),
    path('question_answer/<int:num>/', views.question_answer, name='question_answer'),
    path('question_look', views.question_look, name='question_look'),
    path('question_look/<int:pk>/', views.question_look, name='question_look'),
    path('profile', views.profile, name='profile'),
    path('connect', views.connect, name='connect'),
    path('connectOn/<int:pk>/', views.connectOn, name='connectOn'),
    path('profile/<int:num>/', views.profile, name='profile'),
    path('profile/<str>/<int:num>/', views.profile, name='profile'),
    # path('profile/plot', views.img_plot, name='img_plot'),
    # 勉強部屋
    path('rooms', views.rooms, name='rooms'),
    path('rooms/<str:room_name>/', views.room, name='room'),
    path('rooms/api/<str:room_name>/update',  apis.updateRoom, name='updateRoom'),
    path('rooms/api/<str:room_name>/load',  apis.loadRoom, name='loadRoom')
]

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'solves', SolveViewSet)
