from threading import Thread

import requests
from PyQt6.QtCore import pyqtSignal, QObject


class ExternalSolver(QObject):
    createdAnswer = pyqtSignal(dict)

    def __init__(self, ip_address ,solver, problem):
        super().__init__()
        self.solver = solver
        self.problem = problem
        self.ip_address = ip_address

    def solve(self, callback = None):
        def start_post():
            url = f"http://{self.ip_address}/solve"

            data = {
                "solver": self.solver,
                "problem": self.problem
            }


            post = requests.post(url, json=data, proxies={"http": None, "https": None})
            if not(post.status_code == 200):
                print("Error", post.text)
                if post.status_code == 500:
                    print("Solverが失敗しています")
                return


            self.createdAnswer.connect(callback)
            self.createdAnswer.emit(post.json())

        thread = Thread(target = start_post)
        thread.start()
