import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import color
import time
import requests
import voice_recognition
import threading
import re
import base64
import hashlib
from Crypto.Cipher import AES
from requests.auth import HTTPBasicAuth

class PictureRecognition:
    def __init__(self, root):
        self.cascade_path = './opencv/data/haarcascades/haarcascade_fullbody.xml'
        self.root = root
        self.root.title("Picture Recognition")
        self.label = tk.Label(root)
        self.label.pack()
        self.text_label = tk.Label(root, text="画像・音声認識コーナです。", font=("Helvetica", 40))
        self.text_label.pack()
        self.text_announce_1 = tk.Label(root, text="マイページのQRコードをスキャンしてください。", font=("Helvetica", 20))
        self.text_announce_1.pack()
        self.text_announce_2 = tk.Label(root, text="10秒間認識いたします。", font=("Helvetica", 20))
        self.text_announce_2.pack()
        self.text_announce_3 = tk.Label(root, text="※映像に関しては一切保存はしておりません。", font=("Helvetica", 20))
        self.text_announce_3.pack()
        self.cap = cv2.VideoCapture(0)
        self.cascade = cv2.CascadeClassifier(self.cascade_path)
        self.recognition_duration = 10
        self.dark_overlay = None
        self.task()
    
    def task(self):
        key = b'Enter your key here'
        QR_input = input().strip()
        iv = QR_input[:24]
        print (iv)
        crypted = QR_input[24:]
        print (crypted)
        self.id = 1
        key_dg = hashlib.sha256(key).digest()
        cipher = AES.new(key_dg, AES.MODE_CBC, base64.b64decode(iv))
        crypted = base64.b64decode(crypted)
        prompt = cipher.decrypt(crypted)
        prompt = prompt.rstrip(b'\0')
        prompt = prompt.decode("utf-8")
        self.id = prompt.split(",")[0][1:]
        print(str(self.id) + "への送信を開始します.......")
        self.dark_overlay = None
        self.time = time.time()
        thread1 = threading.Thread(target=self.voice_task)
        thread1.start()
        self.process_frame()
        self.closest_color = None
        self.task()

    def voice_task(self):
        self.voice = voice_recognition.VoiceRecognition(7)
        self.voice.recognition()

    def process_frame(self):
        ret, frame = self.cap.read()
        if time.time() - self.time < self.recognition_duration:

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bodies = self.cascade.detectMultiScale(gray)

                for (x, y, w, h) in bodies:
                    body_roi = frame[y:y+h, x:x+w]
                    resized_roi = cv2.resize(body_roi, (100, 100))
                    hsv_roi = cv2.cvtColor(resized_roi, cv2.COLOR_BGR2HSV)
                    flattened_roi = hsv_roi.reshape(-1, 3)
                    colors, counts = np.unique(flattened_roi, axis=0, return_counts=True)
                    most_common_color = colors[np.argmax(counts)]
                    try:
                        r, g, b = int(most_common_color[0]), int(most_common_color[1]), int(most_common_color[2])
                        self.closest_color = color.get_approximate_color_name((r, g, b))
                        print(self.closest_color)
                    except:
                        print("服装認識エラー")

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.label.config(image=img)
                self.label.image = img
            self.root.after(10, self.process_frame)
        else:
                self.create_dark_overlay()
                if not self.id is None:
                    if self.id.isdigit():
                        url = "http://127.0.0.1:3000/users/" + self.id + "/updatePronpt"
                        data = {"image_recognition": self.closest_color , "voice_recognition_brightness": self.voice.amplitude , "voice_recognition_weather": self.voice.dominant_frequency}
                        response = requests.patch(url, auth=HTTPBasicAuth("user", "pass"), data=data)
                        if response.status_code == 200:
                            print('Update successful')
                        else:
                            print('Update failed')
                

    def create_dark_overlay(self):
        if self.dark_overlay is None:
            self.dark_overlay = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.rectangle(self.dark_overlay, (0, 0), (640, 480), (53, 53, 53), -1)
            self.dark_overlay = cv2.cvtColor(self.dark_overlay, cv2.COLOR_BGR2RGB)
            dark_img = Image.fromarray(self.dark_overlay)
            dark_img = ImageTk.PhotoImage(image=dark_img)
            self.label.config(image=dark_img)
            self.label.image = dark_img

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = PictureRecognition(root)
    root.mainloop()