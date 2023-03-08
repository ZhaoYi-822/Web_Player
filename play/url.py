from os import path

from play import views

from django.contrib import admin
from django.urls import path
from . import views

app_name = 'play'
urlpatterns = [

    path('upload/',views.video_upload,name='upload'),
     path('index/',views.index,name='index'),
    path('play/',views.play,name='play'),


]
