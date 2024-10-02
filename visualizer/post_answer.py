import sys
import requests
import json
from config import *

class Post():
    def __init__(self,answer_json_name):
        self.config = Config("config.json")
        self.answer_json_name = answer_json_name
        self.post()
    def post(self):
        url = f"http://{self.config.ip_address}:{self.config.port}/answere"

        header = { "Content-Type": "application/json","Procon-Token":self.config.token,}

        try:
            with  open(self.answer_json_name) as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            print("ファイルが見つかりませんでした。")
            exit(1)



        try:
            answer = requests.post(url, headers=header, json=json_data,
                        proxies={"http": None, "https": None})
            if answer.status_code == 200:
                print(f"Success: {answer.text}")
            elif answer.status_code == 400:
                print("リクエストの内容が不十分です")
            elif answer.status_code == 401:
                print("トークンが未取得もしくは不正です")
        except AccessTimeError:
            print("競技時間外です")
            exit(1)

        print(answer.status_code)
