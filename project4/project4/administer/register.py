from django.http import JsonResponse
from common.models import Student, Administer
import json


def dispatcher(request):
    """统一处理请求参数并分派到对应函数"""
    try:
        # 解析请求参数
        if request.method == 'GET':
            request.params = request.GET
        elif request.method in ['POST', 'PUT', 'DELETE']:
            try:
                request.params = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'ret': 1, 'msg': '1请求体必须是有效的JSON格式'})
        else:
            return JsonResponse({'ret': 1, 'msg': '2不支持的HTTP方法'})

        # 检查必需参数
        if 'action' not in request.params:
            return JsonResponse({'ret': 1, 'msg': '3缺少action参数'})

        # 分派到对应函数
        action = request.params['action']
        if action == 'list_administers':
            return listadministers(request)
        elif action == 'add_administer':
            return addadminister(request)
        elif action == 'modify_administer':
            return modifyadminister(request)
        elif action == 'del_administer':
            return deleteadminister(request)
        else:
            return JsonResponse({'ret': 1, 'msg': '4不支持的action类型'})

    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'5服务器错误: {str(e)}'})


def listadministers(request):
    """列出所有学生"""
    try:
        students = Administer.objects.all().values('id', 'password')  # 避免返回敏感字段
        return JsonResponse({'ret': 0, 'students': list(students)})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'查询失败: {str(e)}'})


def addadminister(request):
    """添加学生"""
    try:
        # 检查必需字段
        if 'data' not in request.params:
            return JsonResponse({'ret': 1, 'msg': '6缺少data参数'})

        info = request.params['data']
        if 'id' not in info or 'password' not in info:
            return JsonResponse({'ret': 1, 'msg': '7data中必须包含id和password'})

        # 检查学生是否已存在
        if Administer.objects.filter(id=info['id']).exists():
            return JsonResponse({'ret': 1, 'msg': '8学号已存在'})

        # 创建新学生
        student = Administer.objects.create(id=info['id'], password=info['password'])
        return JsonResponse({'ret': 0, 'id': student.id})

    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'9添加失败: {str(e)}'})


def modifyadminister(request):
    """修改学生信息"""
    try:
        # 检查必需字段
        if 'id' not in request.params or 'newdata' not in request.params:
            return JsonResponse({'ret': 1, 'msg': '缺少id或newdata参数'})

        student_id = request.params['id']
        newdata = request.params['newdata']

        # 检查学生是否存在
        try:
            student = Administer.objects.get(id=student_id)
        except Administer.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '学生不存在'})

        # 更新字段（示例：仅允许修改password）
        if 'password' in newdata:
            student.password = newdata['password']
            student.save()
            return JsonResponse({'ret': 0, 'msg': '修改成功'})
        else:
            return JsonResponse({'ret': 1, 'msg': 'newdata中必须包含password字段'})

    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'修改失败: {str(e)}'})


def deleteadminister(request):
    """删除学生"""
    try:
        if 'id' not in request.params:
            return JsonResponse({'ret': 1, 'msg': '缺少id参数'})

        student_id = request.params['id']

        # 检查学生是否存在
        try:
            student = Administer.objects.get(id=student_id)
        except Administer.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '学生不存在'})

        # 删除学生
        student.delete()
        return JsonResponse({'ret': 0, 'msg': '删除成功'})

    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'删除失败: {str(e)}'})