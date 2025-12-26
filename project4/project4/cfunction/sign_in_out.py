'''
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt  # 新增：跨域必加（禁用CSRF验证）
from django.views.decorators.http import require_http_methods  # 新增：限制请求方法
import json
from common.models import Student,Administer



def dispatcher(request):                                # 将请求参数统一放入request 的 params 属性中，方便后续处理

    if request.method == 'GET':                         # GET请求 参数在url中，同过request 对象的 GET属性获取
        request.params = request.GET                        #放到request.params（参数）
    elif request.method in ['POST','PUT','DELETE']:     # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
        request.params = json.loads(request.body)       # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式


    #action = request.params['action']                   # 根据不同的action分派给不同的函数进行处理(哈哈前端没写action)
    if request.method=='GET':           #列出   GET
        return tg(request)
    elif request.method=='POST' or request.method=='OPTIONS':          #添加   POST
        return signin(request)
    elif request.method=='PUT':       #修改   PUT
        return tp(request)
    elif request.method=='DELETE':          #删除   DELETE
        return signout(request)

    else:
        return JsonResponse({'ret': 1, 'administer': '不支持该类型http请求'})



def tg(request):
    pass




def verify_user(user_id, password):
        # 验证学生
        student = Student.objects.filter(id=user_id).first()
        if student and check_password(password, student.password):
            return 'student', student.id

        # 验证管理员
        admin = Administer.objects.filter(id=user_id).first()
        if admin and check_password(password, admin.password):
            return 'administrator', admin.id

        return None, None

def signin(request):
    if request.method != 'POST':
        return JsonResponse({'ret': 1, 'msg': '仅支持POST请求'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'ret': 1, 'msg': '无效的JSON格式'}, status=400)

    if not user_id or not password:
        return JsonResponse({'ret': 1, 'msg': '账号或密码不能为空blank'}, status=400)

    identity, user_id = verify_user(user_id, password)
    if identity:
        request.session['identity'] = identity
        request.session['user_id'] = user_id
        return JsonResponse({'ret': 0, 'identity': identity})
    else:
        return JsonResponse({'ret': 1, 'msg': '账号或密码错误wrong'}, status=401)










"""
# POST
def signin( request):
    # 1. 处理浏览器的OPTIONS预检请求（跨域必做）
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)  # 直接返回200通过预检
    
    try:
        data = json.loads(request.body)  # Django需手动解析JSON请求体
        userId = data.get("id")          # 对应前端传的"id"字段
        passWord = data.get("password")  # 对应前端传的"password"字段
    except json.JSONDecodeError:
        # 处理无效JSON格式（如前端传错数据）
        return JsonResponse({"ret": 1}, status=400)

    # 3. 保留你原有的「空值校验」逻辑
    if not userId or not passWord:
        return JsonResponse({'ret': 1})

    student_user = Student.objects.filter(id=userId).first()
    if student_user is not None:
        # 验证密码（需确保Student模型的password字段是用make_password加密存储的）
        if check_password(passWord, student_user.password):
            # 修正：session存「变量userId」而非字符串"userId"！
            request.session['identity'] = 'student'
            request.session['user_id'] = userId  # 原代码错误：'user_id' = 'userId'（引号会变成固定字符串）
            return JsonResponse({'ret': 0, 'identity': 'student'})
        else:
            # 学生密码错误，继续检查管理员
            pass  # 穿透到下面的管理员逻辑

    # 5. 保留你原有的「管理员验证」逻辑（修正模型类名+密码校验）
    admin_user = Administer.objects.filter(id=userId).first()
    if admin_user is not None:
        if check_password(passWord, admin_user.password):
            request.session['identity'] = 'administrator'
            request.session['user_id'] = userId  # 同样修正：存变量userId
            return JsonResponse({'ret': 0, 'identity': 'administrator'})

    # 6. 所有验证失败（账号不存在/密码错误）
    return JsonResponse({'ret': 1})

    #先检验学生的
    user=Student.objects.filter(id=userId).first()
    if user is not None and user.password:
        if check_password(passWord,user.password):
            request.session['identity'] = 'student'                         # 在session中存入用户类型
            request.session['user_id'] = 'userId'
            return JsonResponse({'ret': 0,'identity':'student'})
        
    else:
        #如果学生不通过则检测管理员的
        user=Administer.objects.filter(id=userId).first()
        if user is not None and user.password:
            if check_password(passWord,user.password):
                request.session['identity'] = 'administer'                  # 在session中存入用户类型
                request.session['user_id'] = 'userId'
                return JsonResponse({'ret': 0,'identity':'administer'})
        else:
            return JsonResponse({'ret': 1})


"""

def tp(request):
    pass




# 登出处理
def signout( request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})
    '''
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from common.models import Student, Administer


@csrf_exempt  # 禁用CSRF验证（仅用于开发，生产环境应使用其他安全措施）
def dispatcher(request):
    # 设置安全的会话cookie属性（应在settings.py中全局设置）
    request.session.set_test_cookie()
    
    try:
        if request.method == 'GET':
            request.params = request.GET
        elif request.method in ['POST', 'PUT', 'DELETE']:
            try:
                request.params = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'ret': 1, 'msg': '无效的JSON格式'}, status=400)
        
        # 分发请求
        if request.method == 'GET':
            return tg(request)
        elif request.method == 'POST':
            return signin(request)
        elif request.method == 'PUT':
            return tp(request)
        elif request.method == 'DELETE':
            return signout(request)
        elif request.method == 'OPTIONS':
            return JsonResponse({'ret': 0}, status=200)  # 简单处理OPTIONS请求
        else:
            return JsonResponse({'ret': 1, 'msg': '不支持该类型HTTP请求'}, status=405)
    
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'服务器错误: {str(e)}'}, status=500)


def tg(request):
    return JsonResponse({'ret': 1, 'msg': '未实现的功能'}, status=501)


def verify_user(user_id, password):
    try:
        # 验证学生
        student = Student.objects.filter(id=user_id).first()
        if student and password==student.password:
            return 'student', student.id

        # 验证管理员
        admin = Administer.objects.filter(id=user_id).first()
        if admin and password==admin.password:
            return 'administrator', admin.id

        return None, None
    except Exception:
        return None, None


@require_http_methods(["POST"])
def signin(request):
    try:
        data = request.params
        user_id = data.get('id')
        password = data.get('password')

        if not user_id or not password:
            return JsonResponse({'ret': 1, 'msg': '账号或密码不能为空blank'}, status=400)

        identity, user_id = verify_user(user_id, password)
        if identity:
            # 设置会话信息(记录用户登录状态，可以在session里面填入其他数据放入缓存来加快速度)
            request.session['identity'] = identity
            request.session['user_id'] = user_id
            request.session.set_expiry(3600)  # 1小时过期
            return JsonResponse({'ret': 0, 'identity': identity})   #会存入Set-cookie到HTTP头里
        else:
            return JsonResponse({'ret': 1, 'msg': '账号或密码错误wrong'}, status=401)
    
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'登录过程中出错: {str(e)}'}, status=500)


def tp(request):
    return JsonResponse({'ret': 1, 'msg': '未实现的功能'}, status=501)


@require_http_methods(["DELETE"])
def signout(request):
    try:
        # 清除会话
        if 'identity' in request.session:
            del request.session['identity']
        if 'user_id' in request.session:
            del request.session['user_id']
        request.session.flush()
        return JsonResponse({'ret': 0})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'登出过程中出错: {str(e)}'}, status=500)