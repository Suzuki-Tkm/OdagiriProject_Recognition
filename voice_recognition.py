import pyaudio
import numpy as np

class VoiceRecognition:
    def __init__(self , time):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.DURATION = time
        self.dominant_frequency = 0
        self.amplitude = 0

    def recognition(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        frames = []
        duration_frames = self.RATE * self.DURATION
        frames_received = 0

        while frames_received < duration_frames:
            data = np.frombuffer(stream.read(self.CHUNK), dtype=np.int16)
            frames.append(data)
            frames_received += len(data)

        frames = np.concatenate(frames)[:duration_frames]
        self.amplitude = np.max(frames)
        frequency = np.fft.rfftfreq(len(frames), d=1.0 / self.RATE)
        spectrum = np.abs(np.fft.rfft(frames))
        self.dominant_frequency = frequency[np.argmax(spectrum)]

        print("大きさ:", self.amplitude)
        print("高さ:", self.dominant_frequency)

        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__": 
    v = VoiceRecognition()
    v.recognition()
