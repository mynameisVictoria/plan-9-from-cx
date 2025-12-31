import json

class JsonStoring:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_name(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            name = dict_data["name"]
            return name
    
    def write_name(self,name):
        with self.file_path.open("r+", encoding="utf-8") as file:
            contents = file.read()
            file.seek(0)
            file.truncate()
            dict_data = json.loads(contents)
            dict_data["name"] = name
            file.write(json.dumps(dict_data))

    def check_name(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            contents = file.read()
            dict_data = json.loads(contents)
            if dict_data["name"] is None:
                return False
            else:
                return True
