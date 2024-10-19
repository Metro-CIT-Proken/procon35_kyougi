
import requests
import json
from config import *
from requests.exceptions import HTTPError, Timeout, RequestException

class Post():
    def __init__(self,answer_json_name,config):
        self.config = config
        self.answer_json_name = answer_json_name
        self.error = ""
        self.post()
    def post(self):
        url = f"http://{self.config.ip_address}:{self.config.port}/answer"


        header = {"Procon-Token":self.config.token}

        try:
            with  open(self.answer_json_name) as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError:
            print("ファイルが見つかりませんでした。")


        try:
            # print(json_data)
            with open ("./answer.json",'w') as file:
                file.write(json.dumps(json_data))
            # print(type(json_data))
            # print("header")
            # print(header)
            # print(len(json_data['ops']))
            answer = requests.post( url, headers=header, json=json_data, proxies={"http": None, "https": None})
            if answer.status_code == 200:
                print(f"Success: {answer.text}")
            elif answer.status_code == 400:
                print("リクエストの内容が不十分です")
            elif answer.status_code == 401:
                print("トークンが未取得もしくは不正です")
            elif answer.status_code == 403:
                print("競技時間外です")


        except Exception as e:
            print("Error exception",e)
            print('Stacktrace',e.filename)
            self.error = e

        # except AccessTimeError:
        #     print("競技時間外です")
        #     exit(1)

