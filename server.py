import socket
import pygame
import random
import threading

song_paths = {
    "song1": "./music/K.O..mp3",
    "song2": "./music/大キック.mp3",
    "song3": "./music/K.O..mp3",
    "song4": "./music/K.O..mp3",
    "song5": "./music/K.O..mp3"
}

usually_song = {
    "song": "/Users/apple/Downloads/test.mp3"
}

def play_music(song_name):
    if song_name in song_paths:
        pygame.mixer.music.load(song_paths[song_name])
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        play_music("usually_song")
    elif song_name == "usually_song":
        pygame.mixer.music.load(usually_song["song"])
        pygame.mixer.music.play(-1)
    else:
        print(f"{song_name} は存在しません。")

def input_handler():
    while True:
        try:
            pronpt = client_socket.recv(1024).decode('utf-8')
            data = selectmusic(pronpt)

            if data in song_paths or data == "usually_song":
                play_music(data)
            else:
                print("無効な曲名です。")
        except:
            print("")

def selectmusic(data):
    if not data.split(",")[0].isdigit():
        voice_recognition_brightness = random.randint(0, 13000)
    else:
        voice_recognition_brightness = float(data.split(",")[0])
    if not data.split(",")[1].isdigit():
        voice_recognition_weather = random.randint(0, 1000)
    else:
        voice_recognition_weather = float(data.split(",")[1])
    print(voice_recognition_brightness)
    print(f"受信したデータ: {data}")
    if voice_recognition_brightness < 1000 or voice_recognition_weather < 100:
        return "song1"
    elif voice_recognition_brightness < 3000 or voice_recognition_weather < 300:
        return "song2"
    elif voice_recognition_brightness < 6000 or voice_recognition_weather < 600:
        return "song3"
    elif voice_recognition_brightness < 9000 or voice_recognition_weather < 900:
        return "song4"
    else:
        return "song5"
    

host = socket.gethostname()
ip = socket.gethostbyname(host)

def client(client_socket):
    pygame.init()
    pygame.mixer.init()
    try:
        input_handler()
    finally:
        pygame.mixer.music.stop()
        pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    server_ip = ip
    server_port = 49162
    print("ip:", ip)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"サーバーが{server_ip}:{server_port}で起動しました。")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"クライアント {client_address} が接続しました。")
        thread1 = threading.Thread(target=client, args=(client_socket,))
        thread1.start()