import requests
import json

URL = 'http://127.0.0.1:8002/restapi/profile_create/'

data = {
    'phone_number': '03204432250',
    'location': 'liberty plaza',
    'user_type': 'professor',
    'user': {'username': 'moe33333', 'first_name': 'moe3333', 'email': 'moe33333@gmail.com', 'password': 'Vend1213'}
}
json_data = json.dumps(data)

r = requests.post(url=URL, data=json_data)
data = r.json
print(data)
