from django.http import JsonResponse
from django.forms.models import model_to_dict
from common.models import Student

def list_student(request):  # 更语义化的函数名（获取单个学生）
    # 1. 仅允许 GET 请求
    if request.method != 'GET':
        return JsonResponse({'ret': 1, 'msg': '仅支持GET请求'})

    # 2. 获取并校验查询参数 `id`
    student_id = request.GET.get('id')
    if not student_id:
        return JsonResponse({'ret': 1, 'msg': '缺少必填参数id'})

    try:
        # 3. 校验 `id` 格式（假设 Student.id 是整数）
        student_id_int = int(student_id)
        # 4. 查询学生（捕获不存在的情况）
        student = Student.objects.get(id=student_id_int)
    except ValueError:
        return JsonResponse({'ret': 1, 'msg': 'id格式错误'})
    except Student.DoesNotExist:
        return JsonResponse({'ret': 1, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'ret': 1, 'msg': f'服务器错误：{str(e)}'})

    # 5. 序列化学生数据（确保包含前端需要的字段，如 name）
    student_data = model_to_dict(student)  # 自动包含模型的所有字段（除了 ManyToMany 等特殊字段）

    # 6. 返回与前端预期一致的响应格式
    return JsonResponse({'ret': 0, 'retlist': student_data})