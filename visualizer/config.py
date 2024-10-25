import json

class Config:
    def __init__(self, file_path):
        self.ip_address = "127.0.0.1"
        self.port = 3000
        self.token = ""
        self.file_path = file_path
        self.solvers = []
        self.pcs=[]
        self.cell_colors = [[255, 0, 0], [0, 0, 255], [0, 255, 0], [255, 255, 0], [167, 87, 168]]
        self.timer_intervals = 1.0


    def save(self):
        config_json = {
            "ip_address":self.ip_address,
            "port":self.port,
            "token":self.token,
            "solvers":self.solvers,
            "pcs":self.pcs,
            "cell_colors": self.cell_colors,
            "timer_intervals": self.timer_intervals
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
        self.pcs = json_data["pcs"]
        self.cell_colors = json_data["cell_colors"]
        self.timer_intervals = json_data["timer_intervals"]

    def ip_address_edited(self,text):
        self.ip_address = text

    def port_edited(self,text):
        self.port = text

    def token_edited(self,text):
        self.token = text

    def timer_edited(self, text):
        self.timer_intervals = text





