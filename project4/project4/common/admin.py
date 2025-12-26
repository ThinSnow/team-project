from django.contrib import admin
from .models import Administer,Student,Material,StudentScore
# Register your models here.


#admini     qcko@gmail.com      12345678
#从/admin里面进入后，可以根据上方的超级用户（开发者账号）来添加数据库里的内容
admin.site.register(Administer)
admin.site.register(Student)
admin.site.register(StudentScore)
admin.site.register(Material)
