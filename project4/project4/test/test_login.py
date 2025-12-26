import  requests,pprint

payload = {
    'id': '111112',
    'password': '123456'
}

response = requests.post('http://localhost:8000/api/cfunction/login',json=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())