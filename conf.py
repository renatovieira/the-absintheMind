import json


def read_db_conf():
    json_data=open('db_config')
    data = json.load(json_data)
    json_data.close()
    print data["password"]
    return data["host"], data["username"], data["password"], data["database"]
