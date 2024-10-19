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

solver = Solve("127.0.0.1", 8080 ,"solver_beam", {
    "board": {
        "width": 16,
        "height": 16,
        "start": [
            "1320122212131201",
            "0013330101213023",
            "2131310000032332",
            "2033113130011103",
            "2022330222031320",
            "3202201120120031",
            "3031212320032332",
            "0211211003120230",
            "0103000120102001",
            "1010003021201231",
            "3131003132303122",
            "0303332223300020",
            "2121102221011021",
            "1133303310003133",
            "0032230321321320",
            "1000101212133002"
        ],
        "goal": [
            "1320122212131201",
            "0031330100233023",
            "2133310002312332",
            "2022113130031103",
            "2002330222021320",
            "3231201110010031",
            "3011212321132332",
            "0203211020121230",
            "0110000103020001",
            "1031003020102231",
            "0300312231101122",
            "0310332232103020",
            "2113222123300121",
            "1133303301302133",
            "0032230310103320",
            "1000101221033002"
        ]
    },
    "general": {
        "n": 2,
        "patterns": [
            {
                "p": 26,
                "width": 4,
                "height": 1,
                "cells": [
                    "1010"
                ]
            },
            {
                "p": 27,
                "width": 2,
                "height": 3,
                "cells": [
                    "00",
                    "00",
                    "11"
                ]
            }
        ]
    }
}
)

def recieve(answer):
    print(answer)

answer = solver.solve(recieve)
print(answer)
