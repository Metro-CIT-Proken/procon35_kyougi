import json

class Config:
    def __init__(self, file_path):
        self.ip_address = "127.0.0.1"
        self.port = 3000
        self.token = ""
        self.file_path = file_path
        self.solvers = []


    def save(self):
        config_json = {
            "ip_address":self.ip_address,
            "port":self.port,
            "token":self.token,
            "solvers":self.solvers,
        }

        json_data = json.dumps(config_json)

        with open(self.file_path, mode='w') as json_file:
            json_file.write(json_data)



    def load(self):
        with open(self.file_path,mode='r') as json_file:
            json_data = json.load(json_file)
        self.ip_address = json_data["ip_address"]
        self.port = json_data["port"]
        self.token = json_data["token"]
        self.solvers = json_data["solvers"]

    def ip_address_edited(self,text):
        self.ip_address = text

    def port_edited(self,text):
        self.port = text

    def token_edited(self,text):
        self.token = text





