from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from common.models import Material,Student



@require_POST  # 仅允许POST请求
def upload_material(request):
    """学生材料上传接口"""
    # --------------------- 1. 接收FormData参数 ---------------------
    # 前端FormData传递的字段：id（学生ID）、material_name、material_type、excepted_score、file（文件）
    student_id = request.POST.get("id")  # 前端用formData.append("id", userId)传递
    material_name = request.POST.get("material_name")
    material_type = request.POST.get("material_type")
    excepted_score = request.POST.get("excepted_score")
    material_file = request.FILES.get("file")  # 文件对象（前端用formData.append("file", selectedFile)）

    # --------------------- 2. 验证必填参数 ---------------------
    if not all([student_id, material_name, material_type, excepted_score, material_file]):
        if not student_id:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：id"})
        if not material_name:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：material_name"})
        if not material_type:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：material_type"})
        if not excepted_score:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：excepted_score"})
        if not material_file:
            return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：material_file"})

        #return JsonResponse({"ret": 1, "msg": "缺少必填参数，请检查：id、material_name、material_type、excepted_score、file"})

    # 验证预期分数格式（需为数字）
    try:
        excepted_score = float(excepted_score)
    except ValueError:
        return JsonResponse({"ret": 1, "msg": "预期分数格式错误，请传入数字"})

    # --------------------- 3. 检查学生是否存在 ---------------------
    try:
        student = Student.objects.get(id=student_id)  # 根据学生ID查询
    except ObjectDoesNotExist:
        return JsonResponse({"ret": 1, "msg": f"学生ID {student_id} 不存在"})

    # --------------------- 4. 保存材料到数据库 ---------------------
    try:
        # 创建Material对象（Django自动处理文件保存到MEDIA_ROOT/materials/）
        Material.objects.create(
            student=student,
            material_name=material_name,
            material_type=material_type,
            excepted_score=excepted_score,
            material_file=material_file  # 直接绑定文件对象
        )
    except Exception as e:
        return JsonResponse({"ret": 1, "msg": f"文件上传失败：{str(e)}"})

    # --------------------- 5. 返回成功响应 ---------------------
    return JsonResponse({"ret": 0})  # 成功返回ret=0