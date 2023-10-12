import requests

user_id = input("ユーザIDを入力してん")
url = "http://127.0.0.1:3000/users/" + user_id + "/updatePronpt"
data = {"image_recognition": "aaaa" , "voice_recognition_brightness": "bbbbb" , "voice_recognition_weather": "cccccc"}

response = requests.patch(url, data=data)

if response.status_code == 200:
    print('Update successful')
else:
    print('Update failed')