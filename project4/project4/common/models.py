from django.db import models
import datetime

# Create your models here.用来存放公共的数据库的定义
# python manage.py makemigrations common  用来定义表的语句
#写完以后再执行python manage.py migrate

#管理员的数据库  //后面的这个modles是这个类的父类（python继承方法
class Administer(models.Model):
    id=models.CharField(max_length=15,primary_key=True)
    password=models.CharField(max_length=20)

#学生的数据库
class Student(models.Model):
    id=models.CharField(max_length=15,primary_key=True)
    password=models.CharField(max_length=20)
    major=models.CharField(max_length=20,default='major')
    name=models.CharField(max_length=20,default='username')
    gpa=models.FloatField(default=0)
    score=models.FloatField(default=0)
    rank=models.IntegerField(default=0)
    

class StudentScore(models.Model):
    student=models.OneToOneField(Student,on_delete=models.CASCADE)
    #学生的各奖项加分情况，单独分出来做关联表
    sci_research=models.FloatField(default=0) #科研成果  
    competition=models.FloatField(default=0)  #学业竞赛      
    creation=models.FloatField(default=0)     #创新创业训练  
    internship=models.FloatField(default=0)   #国际组织实习  
    army=models.FloatField(default=0)         #参军入伍服兵役
    volunteer=models.FloatField(default=0)    #志愿服务  
    honor=models.FloatField(default=0)        #荣誉称号      
    social=models.FloatField(default=0)       #社会工作  
    sport=models.FloatField(default=0)        #体育比赛  








class Material(models.Model):
    material_name=models.CharField(max_length=20,default='material_name')
    material_type=models.CharField(max_length=20,default='material_type')   #PROTECT禁止删除，SET_NULL删后设none
    student=models.ForeignKey(Student,on_delete=models.CASCADE)             #外键设为student,删除学生后材料也删掉
    last_upload_time=models.DateTimeField(default=datetime.datetime.now)    #最新更新时刻（考虑删除
    last_upload_day=models.DateField(default=datetime.datetime.now)         #最新更新日期
    request_upload_time=models.DateTimeField(default=datetime.datetime.now) #上传材料时间（考虑删除
    request_upload_day=models.DateField(default=datetime.datetime.now)      #上传材料日期
    review_upload_time=models.DateTimeField(default=datetime.datetime.now)  #审核材料时间（考虑删除
    review_upload_day=models.DateField(default=datetime.datetime.now)       #审核材料日期
    review_state=models.IntegerField(default=0)                                                                  
    failure_reason=models.CharField(max_length=200,default='material_type')                                      
    review_officer=models.CharField(max_length=20,default='material_type')                                      
    excepted_score=models.FloatField(default=0)
    actual_score=models.FloatField(default=0)
    score=models.FloatField(default=0) 
    material_file = models.FileField(upload_to="", verbose_name="材料文件",default='media/本科生请假单.docx')# 文件保存到 `MEDIA_ROOT/materials/`
