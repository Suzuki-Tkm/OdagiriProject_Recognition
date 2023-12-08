import requests
from requests.auth import HTTPBasicAuth

user_id = input("ユーザIDを入力してん")
# url = "http://127.0.0.1:3000/users/" + user_id + "/updatePicture"
url = "http://127.0.0.1:3000/users/" + user_id + "/updatePicture_dall"#dall用
file_path = '/Users/apple/Downloads/test1.png'  # アップロードするファイルのパス

# files = {'picture': open(file_path, 'rb')}
files = {'picture_dall': open(file_path, 'rb')}#dall用
response = requests.patch(url, auth=HTTPBasicAuth("user", "pass"), files=files)

if response.status_code == 200:
    print('Update successful')
else:
    print('Update failed')