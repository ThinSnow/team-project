from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from common.models import Student,Administer,StudentScore,Material
import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def dispatcher(request): 
    if request.method == 'GET':           #列出   GET
        return get_materials(request)
    elif request.method == 'POST':          #添加   POST
        return get_one_material(request)
    elif request.method == 'PUT':       #修改   PUT
        return update_material(request)
    elif request.method == 'DELETE':          #删除   DELETE
        return delete_material(request)

    else:
        return JsonResponse({'ret': 1, 'administer': '不支持该类型http请求'})










@csrf_exempt
def get_materials(request):
    if request.method != "GET":
        return JsonResponse({"ret": 1, "msg": "仅支持GET请求"})

    materials = Material.objects.all()

    retlist = [
        {
            "id": str(m.student.id),
            'name':m.student.name,
            "material_name": m.material_name,
            "material_type": m.material_type,
            "excepted_score": m.excepted_score,
            "actual_score": m.actual_score,
            "request_upload_time": m.request_upload_time.strftime("%H:%M:%S"),
            "request_upload_day": m.request_upload_time.strftime("%Y-%m-%d"),
            "review_upload_time": m.review_upload_time.strftime("%H:%M:%S") if m.review_upload_time else "",
            "review_upload_day": m.review_upload_day.strftime("%Y-%m-%d") if m.review_upload_day else "",
            "review_state": m.review_state,
            "review_officer": m.review_officer,
            "failure_reason": m.failure_reason or "",
            
        }
        for m in materials
    ]

    return JsonResponse({"ret": 0, "retlist": retlist})













@csrf_exempt
def get_one_material(request):
    # 1. 解析请求体中的JSON参数
    try:
        params = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ret": 1, "msg": "请求体必须是有效的JSON"})

    # 2. 获取前端传入的参数
    student_id = params.get("id")  # 学生ID
    material_name = params.get("material_name")  # 材料名称

    # 3. 验证参数是否完整
    if not student_id or not material_name:
        return JsonResponse({"ret": 1, "msg": "缺少必填参数：id或material_name"})

    # 4. 查询学生是否存在（可选，根据需求决定是否验证学生）
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"学生ID为{student_id}的学生不存在"})

    # 5. 查询材料记录（关键：同时验证student和material_name）
    try:
        # 使用get()查询唯一记录（若需严格唯一性，否则用filter()）
        material = Material.objects.get(student=student, material_name=material_name)
    except Material.DoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"未找到学生ID为{student_id}且材料名为{material_name}的记录"})
    except Material.MultipleObjectsReturned:
        return JsonResponse({"ret": 1, "msg": f"学生ID为{student_id}且材料名为{material_name}的记录不唯一"})

    # 6. 构造返回数据
    ret_data = {
        "id": str(material.student.id),
        'name':student.name,
        "material_name": material.material_name,
        "material_type": material.material_type,
        "excepted_score": material.excepted_score,
        "actual_score": material.actual_score,
        "request_upload_time": material.request_upload_time.strftime("%H:%M:%S") if material.request_upload_time else "",
        "request_upload_day": material.request_upload_time.strftime("%Y-%m-%d") if material.request_upload_time else "",
        "review_upload_time": material.review_upload_time.strftime("%H:%M:%S") if material.review_upload_time else "",
        "review_upload_day": material.review_upload_day.strftime("%Y-%m-%d") if material.review_upload_day else "",
        "review_state": material.review_state,
        "review_officer": material.review_officer,
        "failure_reason": material.failure_reason or "",
    }

    return JsonResponse({"ret": 0, "retlist": [ret_data]})  # 返回列表格式，与前端预期一致


def update_material(request):
    # 1. 解析请求体中的JSON参数
    try:
        params = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ret": 1, "msg": "请求体必须是有效的JSON"})

    # 2. 获取前端传入的参数
    student_id = params.get("id")  # 学生ID
    material_name = params.get("material_name")  # 材料名称
    newdata = params.get("newdata")  # 修正：从params获取newdata

    # 3. 验证参数是否完整
    if not all([student_id, material_name, newdata]):
        return JsonResponse({"ret": 1, "msg": "缺少必填参数：id、material_name或newdata"})

    # 4. 查询学生对象（假设student_id是Student模型的外键或主键）
    try:
        student = Student.objects.get(id=student_id)  # 或根据实际字段名调整
    except Student.DoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"未找到学生ID为{student_id}的记录"})

    # 5. 查询材料记录（严格验证student和material_name）
    try:
        material = Material.objects.get(student=student, material_name=material_name)
    except Material.DoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"未找到学生ID为{student_id}且材料名为{material_name}的记录"})
    except Material.MultipleObjectsReturned:
        return JsonResponse({"ret": 1, "msg": f"学生ID为{student_id}且材料名为{material_name}的记录不唯一"})

    # 6. 动态更新字段（避免重复if判断）
    update_fields = []
    for field, value in newdata.items():
        if hasattr(material, field):  # 检查字段是否存在
            setattr(material, field, value)
            update_fields.append(field)
        else:
            return JsonResponse({"ret": 1, "msg": f"无效字段: {field}"})

    # 7. 保存到数据库
    try:
        material.save(update_fields=update_fields)  # 指定更新的字段以提高性能
    except Exception as e:
        return JsonResponse({"ret": 1, "msg": f"数据库保存失败: {str(e)}"})

    return JsonResponse({"ret": 0, "msg": "更新成功"})



def delete_material(request):
    if request.method != "DELETE":
        return JsonResponse({"ret": 1, "msg": "仅支持POST请求"})
    """删除材料接口（基于Student外键）"""
    try:
        req_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ret": 1, "msg": "无效的JSON格式，请检查请求体"})

    user_id = req_data.get("user_id")
    material_name = req_data.get("material_name")

    if not user_id or not material_name:
        if not user_id:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数：user_id"})
        if not material_name:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数：material_name"})

    # --------------------- 修正点：通过Student外键查询 ---------------------
    try:
        # 检查学生是否存在（可选，根据业务需求）
        student = Student.objects.get(id=user_id)
    except Student.DoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"学生ID {user_id} 不存在"})

    # 通过外键关联查询材料（确保只删除该学生的材料）
    material_queryset = Material.objects.filter(
        student_id=user_id,  # 直接使用外键字段（如student_id）
        material_name=material_name
    )

    if not material_queryset.exists():
        return JsonResponse({"ret": 1, "msg": f"未找到学生ID为{user_id}的对应材料"})

    try:
        material_queryset.delete()
    except IntegrityError as e:
        return JsonResponse({"ret": 1, "msg": f"删除失败：{str(e)}"})
    except Exception as e:
        return JsonResponse({"ret": 1, "msg": f"删除失败：未知错误-{str(e)}"})

    return JsonResponse({"ret": 0})