import requests

url = 'http://127.0.0.1:3000/users/1/updatePicture'
data = {'user_id': 1, 'name': 'test'}

response = requests.patch(url, data=data)

if response.status_code == 200:
    print('Update successful')
else:
    print('Update failed')