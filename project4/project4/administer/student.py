from django.http import JsonResponse
from common.models import Student,Administer,Material
import json



#用来抓取对应请求的函数
def dispatcher(request):                                # 将请求参数统一放入request 的 params 属性中，方便后续处理

    if request.method == 'GET':                         # GET请求 参数在url中，同过request 对象的 GET属性获取
        request.params = request.GET                        #放到request.params（参数）
    elif request.method in ['POST','PUT','DELETE']:     # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
        request.params = json.loads(request.body)       # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式


    action = request.params['action']                   # 根据不同的action分派给不同的函数进行处理
    if action == 'list_students':           #列出   GET
        return liststudents(request)
    elif action == 'add_students':          #添加   POST
        return addstudents(request)
    elif action == 'modify_students':       #修改   PUT
        return modifystudents(request)
    elif action == 'del_students':          #删除   DELETE
        return deletestudents(request)

    else:
        return JsonResponse({'ret': 1, 'administer': '不支持该类型http请求'})





def liststudents(request):
    qs=Student.objects.values()                         #返回一个QuerySet对象，包含所有表记录
    retlist=list(qs)                                    #用内置函数将上述返回的对象转化成list类型，可转化为JSON字符串
    return JsonResponse({'ret':0,'retlist':retlist})    #传给前端
    

def addstudents(request):                               #用来注册，一开始只有学号和密码，暂时不写csf校验
    info=request.params['data']                         #目前这里只放这些，不知道不写的后果
    record=Student.objects.create(id=info['id'],password=info['password'])
    return JsonResponse({'ret':0,'id':record.id})       #返回值记得和前端统一                                             


def modifystudents(request):
    studentid = request.params['id']                    # 从请求消息中 获取修改客户的信息
    newdata    = request.params['newdata']              # 找到该客户，并且进行修改操作
    try:                                                # 根据 id 从数据库中找到相应的客户记录 
        student = Student.objects.get(id=studentid)
    except Student.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{studentid}`的客户不存在'
        }

    if 'major' in  newdata:
        student.major = newdata['major']
    if 'name' in  newdata:
        student.name = newdata['name']
    if 'gpa' in  newdata:
        student.gpa = newdata['gpa']
    if 'score' in  newdata:
        student.score = newdata['score']
    if 'rank' in  newdata:
        student.rank = newdata['rank']
    student.save()                                  # 把改好的这个对象存到数据库里面
    return JsonResponse({'ret': 0})


def deletestudents(request):
    studentid = request.params['id']
    try:                                            # 根据 id 从数据库中找到相应的客户记录
        student = Student.objects.get(id=studentid)
    except Student.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{studentid}`的客户不存在'
        }
    student.delete()                                # delete 方法就将该记录从数据库中删除了
    return JsonResponse({'ret': 0})




'''
def person(request):
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'Not GET'})
    try:
        id=request.params['id']
        student_number=Administer.objects.count()
        pending_number=Material.objects.filter(review_state=0).count()
        reviewed_number=Material.objects.count()-pending_number
    except Administer.DoesNotExist:
        return JsonResponse({'ret':1,'msg':id+'not exist'})
    
    retlist=[
        {
            'id':id,
            'student_number':student_number,
            'pending_number':pending_number,
            'reviewed_number':reviewed_number
        }
    ]
    return JsonResponse({'ret':0,'retlist':retlist})
'''



def person(request):
    # 1. 校验请求方法
    if request.method != 'GET':
        return JsonResponse(
            {'ret': 1, 'msg': 'Method not allowed'},
            status=405
        )
    
        #admin = Administer.objects.get(id=admin_id)
        # 3. 统计数据
    student_number = Student.objects.count()  # 学生总数
    pending_count = Material.objects.filter(review_state=0).count()  # 待审核材料数
    reviewed_count = Material.objects.exclude(review_state=0).count()  # 已审核材料数


    # 4. 构造响应数据（返回 id 而不是 name）
    response_data = {
        'ret': 0,
        'retlist': {  # 保持 Mock 格式（retlist 是对象）
            'name': '默认名称',  # 直接返回 id，而不是 name
            'student_number': student_number,
            'pending_number': pending_count,
            'reviewed_number': reviewed_count
        }
    }

    return JsonResponse(response_data)