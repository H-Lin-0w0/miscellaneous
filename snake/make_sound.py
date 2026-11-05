import math
import os
import struct
import wave

RATE = 44100
SOUND_DIR = os.path.dirname(os.path.abspath(__file__))   # 这个脚本所在的文件夹


def make_beep(filename, freq, duration):
	with wave.open(filename, "w") as w:
		w.setnchannels(1)
		w.setsampwidth(2)
		w.setframerate(RATE)
		for i in range(int(RATE * duration)):
			value = int(12000 * math.sin(2 * math.pi * freq * i / RATE))
			w.writeframes(struct.pack("<h", value))


make_beep(os.path.join(SOUND_DIR, "eat.wav"), 880, 0.1)
make_beep(os.path.join(SOUND_DIR, "die.wav"), 220, 0.4)