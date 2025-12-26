import  requests,pprint
# 1. 普通字段（用data传递，对应后端request.POST）
data = {
    "id": "22920242200001",         # 与后端request.POST.get("id")对应
    "material_name": "测试材料",     # 注意：material_name应该是字符串（你之前写的1可能类型错误）
    "material_type": "2",            # 按后端要求传字符串或数字（后端会转）
    "excepted_score": 3            # 后端会转float，传字符串/数字都可以
}

# 2. 文件字段（用files传递，对应后端request.FILES）
# 注意：文件需用二进制模式打开（rb），且路径要正确
files = {
    "file": open("media/test.txt", "rb")  # 键名"file"必须与后端request.FILES.get("file")一致
}

# 3. 发送请求（无需手动设置Content-Type，requests会自动处理）
url = "http://localhost:8000/api/student/addfile"
response = requests.post(url, data=data, files=files)

# 4. 打印结果（调试用）
print("status:", response.status_code)
print("response:", response.text)
pprint.pprint(response.json())