import requests

class Solve:
    def __init__(self, ip_address, port ,solver, problem):
        self.solver = solver
        self.problem = problem
        self.ip_address = ip_address
        self.port = port

    def solve(self, callback = None):
        url = f"http://{self.ip_address}:{self.port}/solve"

        data = {
            "solver": self.solver,
            "problem": self.problem
        }


        try:
            post = requests.post(url, json=data, proxies={"http": None, "https": None})
            if not(post.status_code == 200):
                print("Error", post.text)

            if callback != None:
                callback(post.json())
        except Exception as e:
            print("Error exception",e)
            print('Stacktrace',e.filename)
            self.error = e



def recieve(answer):
    print(answer)

