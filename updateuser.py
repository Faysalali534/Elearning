import requests
import json

URL = 'http://127.0.0.1:8002/restapi/update_user/'

data = {
    'id': 55,
    'phone_number': '03204432255',
    'location': 'liberty plazaa',
    'user_type': 'professor'
}
json_data = json.dumps(data)

r = requests.put(url=URL, data=json_data)
data = r.json
print(data)
