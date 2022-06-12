from django.urls import path

from . import views
from .api import apis

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('api/<str:room_name>/update',  apis.updateRoom, name='updateRoom'),
    path('api/<str:room_name>/load',  apis.loadRoom, name='loadRoom')
]