from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from common.models import Student,Administer,StudentScore,Material
import datetime
import json

# award.py 中新增函数（或修改现有函数）
def listawards(request):
    try:
        # 1. 查询所有学生的奖励分数（关联Student表）
        # select_related("student")：优化关联查询，避免N+1问题
        score_records = StudentScore.objects.select_related("student").all()

        # 2. 构造retlist（按前端要求格式）
        retlist = []
        for record in score_records:
            retlist.append({
                "id": record.student.id,  # 关联Student表的id
                "sci_research": record.sci_research,
                "competition": record.competition,
                "creation": record.creation,
                "internship": record.internship,
                "army": record.army,
                "volunteer": record.volunteer,
                "honor": record.honor,
                "social": record.social,
                "sport": record.sport
            })

        # 转换为北京时间（localtime处理时区）
        local_upload_time = localtime(timezone.now())
        last_upload_day = local_upload_time.strftime("%Y-%m-%d")
        last_upload_time = local_upload_time.strftime("%H:%M:%S")
        # 4. 返回符合要求的JSON响应
        return JsonResponse({
            "ret": 0,
            "last_upload_day": last_upload_day,
            "last_upload_time": last_upload_time,
            "retlist": retlist
        })

    except Exception as e:
        # 异常处理（返回错误信息）
        return JsonResponse({
            "ret": 1,
            "msg": f"获取奖励信息失败：{str(e)}"
        })



def liststudents(request):
    try:
        # 1. 查询所有学生并按 score 降序排序
        students = Student.objects.all().order_by('-score')
        
        # 2. 动态计算 rank（如果 score 相同，rank 也相同）
        rank = 1
        prev_score = None
        student_list = []
        
        for idx, student in enumerate(students):
            if student.score != prev_score:
                rank = idx + 1  # 更新排名（如果分数不同）
                prev_score = student.score
            
            student.rank=rank
            student.save()
            # 添加 rank 到学生数据
            student_data = {
                "id": student.id,
                "name": student.name,
                "score": student.score,
                "rank": rank,
                "major":student.major,
                "gpa":student.gpa,
            }
            student_list.append(student_data)
        
        # 3. 返回 JSON 响应
        return JsonResponse({
            'ret': 0,
            'retlist': student_list
        })
    
    except Exception as e:
        return JsonResponse({
            'ret': 1,
            'msg': f'查询失败: {str(e)}'
        })
    



@csrf_exempt
def get_materials(request):
    if request.method != "GET":
        return JsonResponse({"ret": 1, "msg": "仅支持GET请求"})

    student_id = request.GET.get("id")
    if not student_id:
        return JsonResponse({"ret": 1, "msg": "缺少必填参数student_id"})

    materials = Material.objects.filter(student=student_id)
    if not materials.exists():
        return JsonResponse({"ret": 1, "msg": f"未找到学生ID为{student_id}的材料"})

    retlist = [
        {
            "id": str(m.id),
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




def delete_material(request):
    if request.method != "POST":
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