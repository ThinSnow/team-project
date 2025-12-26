from django.urls import path
from student import register,personal,award,files
#from .views import index

urlpatterns = [
    #测试
    #path('index/', index),
    path('register',register.dispatcher),
    path('personal',personal.list_student),
    path('information',award.liststudents),
    path('award',award.listawards),
    path('material',award.get_materials),
    path('deletem',award.delete_material),
    path('addfile',files.upload_material),
]

