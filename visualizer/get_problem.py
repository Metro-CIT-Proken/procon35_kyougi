import requests
from config import *


class Get():
    def __init__(self):
        self.config = Config("config.json")
        self.main

    def main(self):
        url = f"http://{self.config.ip_address}:{self.config.port}/problem"


        header = {"Procon-Token": self.config.token}

        try:
            response = requests.get(url,headers=header,proxies={"http": None, "https": None})
            self.response_text = response.text
            # response = requests.get(url,headers=header)
            if response.status_code == 200:
                print('Success',response.text)
            elif response.status_code == 401:
                print("401: トークンが指定されていない、もしくは不正です。")
            else:
                print("Failed with status code:",response.status_code)
        except requests.exceptions.RequestException as e :
            print('Error', e)
        except AccessTimeError :
            print("403: 競技時間外です")
