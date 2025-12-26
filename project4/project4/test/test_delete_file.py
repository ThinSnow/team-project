import  requests,pprint

payload = {
    'user_id': '22920242200001',
    "material_name":'1',
}

response = requests.post('http://localhost:8000/api/student/deletem',json=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())