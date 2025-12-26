import  requests,pprint

payload = {
    'id': '22920242200001',
}

response = requests.get('http://localhost:8000/api/student/personal',params=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())