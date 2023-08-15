import tkinter as tk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        root.attributes('-fullscreen', True)
        # self.root.geometry("300x100")

        self.message = tk.Label(
            root,
            text="",
            font=("", 50),
        )
        self.message.place(relx=0.5, rely=0.3, anchor="center")

        self.label = tk.Label(
            root,
            text="",
            font=("", 180),
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.start()

    def update_label(self, remaining_time):
        if remaining_time > 0:
            self.message.config(text=f"画像認識と音声認識をはじめます。あなたの渾身の一発芸まで")
            self.label.config(text=f"{remaining_time} seconds")
            self.root.after(1000, self.update_label, remaining_time - 1)
        else:
            self.label.config(text="Timer done!")
            self.run_recognition()
            
    def run_recognition(self):
        # 音声認識と画像認識
        print("音声認識と画像認識")

    def start(self):
        self.update_label(10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()