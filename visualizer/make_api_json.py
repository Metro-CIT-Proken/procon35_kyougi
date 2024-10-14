import json
import sys

args = sys.argv

try:
    file_path = args[1]
except IndexError:
    print("引数が足りません")

with open(file_path) as json_problem:
    problem = json.load(json_problem)

teams = []


while(1):
    team = input("teams: ")
    if team == "q":
        break
    teams.append(team)

duration = int(input("duration: "))

api_json_data = {
    "teams": teams,
    "duration": duration,
    "problem": problem,
  }


api_json = json.dumps(api_json_data)
print(api_json)


directory_place = input("jsonファイルが入るディレクトリを選択してください: ")
with open(directory_place+'/'+input("ファイル名を入力してください"),mode='w' ) as json_new_file:
    json_new_file.write(api_json)




