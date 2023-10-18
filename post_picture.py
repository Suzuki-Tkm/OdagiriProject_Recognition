import requests
from requests.auth import HTTPBasicAuth

user_id = input("ユーザIDを入力してん")
url = "http://127.0.0.1:3000/users/" + user_id + "/updatePicture"
file_path = '/Users/apple/Downloads/7FUCBcl__400x400.png'  # アップロードするファイルのパス

files = {'picture': open(file_path, 'rb')}
response = requests.patch(url, auth=HTTPBasicAuth("user", "pass"), files=files)

if response.status_code == 200:
    print('Update successful')
else:
    print('Update failed')