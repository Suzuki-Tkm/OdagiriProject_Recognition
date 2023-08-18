import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import color

class PictureRecognition:
    def __init__(self, root):
        self.cascade_path = './opencv/data/haarcascades/haarcascade_fullbody.xml'
        self.root = root
        self.root.title("Picture Recognition")
        self.label = tk.Label(root)
        self.label.pack()
        self.cap = cv2.VideoCapture(0)
        self.cascade = cv2.CascadeClassifier(self.cascade_path)
        self.cnt = 10
        self.temp = 0
        self.process_frame()

    def process_frame(self):
        ret, frame = self.cap.read()
        if self.cnt < self.temp:
            self.cap.release()
            cv2.destroyAllWindows()
            return
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
                    closest_color = color.get_approximate_color_name((r, g, b))
                    print(closest_color)
                    self.temp += 1
                except:
                    print("服装認識エラー")

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.label.config(image=img)
            self.label.image = img

        self.root.after(10, self.process_frame)

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = PictureRecognition(root)
    root.mainloop()