import  requests,pprint

payload = {
    'action' : 'add_administer',
    'data':{
        'id': '111113',
        'password': '123456',
    }
}

response = requests.post('http://localhost:8000/api/administer/register',json=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())