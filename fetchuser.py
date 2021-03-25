import requests
import json

# URL = 'http://127.0.0.1:8002/restapi/user_profile_api/'

URL = 'http://127.0.0.1:8002/restapi/users_data_api/'


def get_data(pk=None):
    data = {}
    if pk is not None:
        data = {'id': pk}
    json_data = json.dumps(data)
    headers = {'content-Type': 'application/json'}
    r = requests.get(url=URL, headers=headers, data=json_data)
    data = r.json()
    print(data)


get_data(30)


def post_data():
    data = {
        'phone_number': '03204432250',
        'location': 'liberty plaza',
        'user_type': 'professor',
        'user': {'username': 'moe33337', 'first_name': 'moe3337', 'email': 'moe33337@gmail.com', 'password': 'Vend1213'}
    }
    json_data = json.dumps(data)

    r = requests.post(url=URL, data=json_data)
    data = r.json
    print(data)


def put_data(idd):
    data = {
        'id': idd,
        'phone_number': '03204432255',
        'location': 'liberty plazaa',
        'user_type': 'professor'
    }
    json_data = json.dumps(data)

    r = requests.put(url=URL, data=json_data)
    data = r.json
    print(data)


def delete_data(idd):
    data = {}
    if idd:
        data = {'id': idd}
    json_data = json.dumps(data)
    r = requests.delete(url='http://127.0.0.1:8002/restapi/users_profile/', data=json_data)
    data = r.json()
    print(data)


# post_data()
