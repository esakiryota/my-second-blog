from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('find/<str>/<int:num>/', views.find, name='find'),
    path('find/', views.find, name='find'),
    path('category/', views.category, name='category'),
    path('category/<str>', views.category, name='category'),
    path('category/<str>/<int:num>/', views.category, name='category'),
    path('<int:num>', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('student', views.student, name='student'),
    path('test', views.test, name='test'),
]
