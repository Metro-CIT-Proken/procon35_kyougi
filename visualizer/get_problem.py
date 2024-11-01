import requests
from mainwidget import *
from config import *
import json
class Get():
    def __init__(self,config):
        self.config = config
        self.start_board = [[]]
        self.goal_board = [[]]
        self.board_width = 0
        self.board_height = 0
        self.status_code = 0
        self.error = ""
        self.main()


    def main(self):
        url = f"http://{self.config.ip_address}:{self.config.port}/problem"


        header = { "Procon-Token": self.config.token }


        try:
            response = requests.get(url, headers=header, proxies={"http": None, "https": None})
            self.status_code = response.status_code
            # response = requests.get(url,headers=header)
            if response.status_code == 200:

                self.problem = json.loads(response.text)
                self.board_width = self.problem['board']['width']
                self.board_height =self.problem['board']['height']
                self.start_board = [[ int(self.problem['board']['start'][y][x]) for x in range(self.board_width)]for y in range(self.board_height)]#スタート盤面
                self.goal_board = [[ int(self.problem['board']['goal'][y][x]) for x in range(self.board_width)]for y in range(self.board_height)]
                self.fixed_form_num = self.problem['general']['n']
                self.fixed_form_numbers = [ self.problem['general']['patterns'][x]['p'] for x in range(self.fixed_form_num)]
                self.fixed_form_widths = { self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['width'] for x in range(self.fixed_form_num)}
                self.fixed_form_heights = {self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['height'] for x in range(self.fixed_form_num)}
                self.fixed_form_cells = {self.fixed_form_numbers[x] : [ [self.problem['general']['patterns'][x]['cells'][i][j] for
                                j in range(len(self.problem['general']['patterns'][x]['cells'][i]))]for i in range(len(self.problem['general']['patterns'][x]['cells'])) ]
                            for x in range(self.fixed_form_num)}
            elif response.status_code == 400:
                print("リクエストの内容が不十分です")
            elif response.status_code == 401:
                print("トークンが未取得もしくは不正です")
            elif response.status_code == 403:
                print("競技時間外です")
            else:
                print("Failed with status code:",response.status_code)
                return 1
        except requests.exceptions.RequestException as e :
            print('Error',e)
            print('Stacktrace',e.filename)
            self.error = e
            # exit(1)

class GetByHand():
    def __init__(self, problem):
        self.status_code = 100
        self.error = ""

        self.problem = problem
        self.board_width = self.problem['board']['width']
        self.board_height =self.problem['board']['height']
        self.start_board = [[ int(self.problem['board']['start'][y][x]) for x in range(self.board_width)]for y in range(self.board_height)]#スタート盤面
        self.goal_board = [[ int(self.problem['board']['goal'][y][x]) for x in range(self.board_width)]for y in range(self.board_height)]
        self.fixed_form_num = self.problem['general']['n']
        self.fixed_form_numbers = [ self.problem['general']['patterns'][x]['p'] for x in range(self.fixed_form_num)]
        self.fixed_form_widths = { self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['width'] for x in range(self.fixed_form_num)}
        self.fixed_form_heights = {self.fixed_form_numbers[x] : self.problem['general']['patterns'][x]['height'] for x in range(self.fixed_form_num)}
        self.fixed_form_cells = {self.fixed_form_numbers[x] : [ [self.problem['general']['patterns'][x]['cells'][i][j] for
                        j in range(len(self.problem['general']['patterns'][x]['cells'][i]))]for i in range(len(self.problem['general']['patterns'][x]['cells'])) ]
                    for x in range(self.fixed_form_num)}
