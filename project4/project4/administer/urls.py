from django.urls import path
from .views import list
from administer import student,register,file      

urlpatterns = [
    path('list/', list),
    path('student',student.dispatcher),             #专门用来处理学生的信息
    path('person',student.person),
    path('register',register.dispatcher),
    path('getm',file.dispatcher),
]














