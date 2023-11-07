import socket
import requests
import re
import base64
import hashlib
from Crypto.Cipher import AES
from requests.auth import HTTPBasicAuth

######################
#追加して
server_ip = input("serverのipアドレスを入力して")
server_port = 49161

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))
print(f"サーバーに接続しました。")
#######################


while True:
    key = b'Enter your key here'
    QR_input = input().strip()
    iv = QR_input[:24]
    print (iv)
    crypted = QR_input[24:]
    print (crypted)
    key_dg = hashlib.sha256(key).digest()
    cipher = AES.new(key_dg, AES.MODE_CBC, base64.b64decode(iv))
    crypted = base64.b64decode(crypted)
    prompt = cipher.decrypt(crypted)
    prompt = prompt.rstrip(b'\0')
    prompt = prompt.decode("utf-8")
    id = prompt.split(",")[0][1:]
    print(prompt)

    ######################
    #追加して
    message = prompt.split(",")[10] + "," +prompt.split(",")[11]
    client_socket.send(message.encode('utf-8'))
    #######################
    
    if message.lower() == 'exit':
        break


######################
#追加して
client_socket.close()
#######################