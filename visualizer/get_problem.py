import requests
class Get():
    def __init__():
    url = "http://localhost:3000/problem"


    header = {"Procon-Token":str(input("トークンを入力してください"))}

    try:
        response = requests.get(url,headers=header,proxies={"http": None, "https": None})
        # response = requests.get(url,headers=header)
        if response.status_code == 200:
            print('Success',response.text)
        else:
            print("Failed with status code:",response.status_code)
    except requests.exceptions.RequestException as e :
        print('Error',e)
