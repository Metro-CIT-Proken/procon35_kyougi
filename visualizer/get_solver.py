import requests
import json

class GetSolver:
    def __init__(self,ip_address,port):
        self.ip_address = ip_address
        self.port = port
        self.main()


    def main(self):
        url = f"http://{self.ip_address}:{self.port}/get_solvers"

        try:
            response = requests.get(url,proxies={"http":None,"https":None})
            print(response.text)
            self.solvers = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print('Error get_solver', e)

GetSolver("127.0.0.1",8080)




