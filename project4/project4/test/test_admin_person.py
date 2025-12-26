import  requests,pprint



payload = {
    'id':'111111'
}

response = requests.get('http://localhost:8000/api/administer/person',params=payload)

print('status:',response.status_code)
print('response:',response.text)

pprint.pprint(response.json())