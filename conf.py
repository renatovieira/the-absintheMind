import json


def read_db_conf():
    json_data=open('db_config')
    data = json.load(json_data)
    json_data.close()
    return data["host"], data["username"], data["password"], data["database"]


def read_url():
    json_data=open('db_config')
    data = json.load(json_data)
    json_data.close()
    return data.get('url', "http://localhost:5000")

url = read_url()