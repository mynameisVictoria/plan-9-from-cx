import json

class JsonStoring:
    def __init__(self):
        pass

    @staticmethod
    def read_name():
        with open("user_data.json", "r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            name = dict_data["name"]
            return name
    @staticmethod
    def write_name(name):
        with open("user_data.json","r+", encoding="utf-8") as file:
            contents = file.read()
            file.seek(0)
            file.truncate()
            dict_data = json.loads(contents)
            dict_data["name"] = name
            file.write(json.dumps(dict_data))
