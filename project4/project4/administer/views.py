from django.shortcuts import render
from django.http import HttpResponse
from common.models import Student


# Create your views here.
''''''
#列出特定的学生（用作个人中心的练习
def list(request):                      #objects是类自带的属性，用来管理此类对应数据库；
    qs=Student.objects.values('id')  #values是方法，返回一个QuerySet对象，包含所有表记录，每条表记录都是一个dict（字典）对象。如果只要返回几个参数，只需要在括号里面填相应参数就可以了(记得对应参数要加引号)

    ph=request.GET.get('id',None)       #检查是否有id参数，如果有则添加过滤条件(GET表示GET请求，get表示get方法，后面指的是返回id，若无id则返回none)

    if ph:                              #若无上面列出的参数，则不过滤
        qs=qs.filter(id=ph)             #添加过滤条件
    
    #遍历qs，下面那个在定义返回字符串      
    retStr=''                           
    for student in qs:
        for id,value in student.items():
            retStr += f'{id}:{value}|'
        retStr+='<br>'

    return HttpResponse(retStr)








































