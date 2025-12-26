import  requests,pprint

payload = {
    'action':'modify_students',
    'id':'22920242200004',
    'gpa':1
}

response = requests.put('http://localhost:8000/api/administer/student',json=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())