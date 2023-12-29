import math
import pyaudio
import numpy as np

p = pyaudio.PyAudio()

buffer_size = 2048

volume = 0.5
fs = 44100
duration = 60.0

base_frequency = 115.0
# delta - 1-4 Hz
# theta - 4-8 Hz
# alpha - 8-14 Hz
# beta - 14-30 Hz
# gamma - 30-100 Hz
# gamma / beta are where it gets interesting
beat_frequency = 30.0

f_left = base_frequency - beat_frequency / 2.0
f_right = base_frequency + beat_frequency / 2.0


def sin(freq: float, duration: float):
    return (np.sin(2 * np.pi * np.arange(fs * duration) * freq / fs)).astype(np.float32)


placebo = False

samples_left = sin(f_left, duration)
samples_right = sin(f_right, duration)

if not placebo:
    samples = np.array([samples_left, samples_right]).T
else:
    samples = np.array(samples_left + samples_right) * 0.5


runs = math.ceil(duration / 10.0)


output_bytes = (volume * samples).tobytes()

stream = p.open(
    format=pyaudio.paFloat32,
    channels=2 if not placebo else 1,
    rate=fs,
    output=True,
    frames_per_buffer=buffer_size,
)
stream.write(output_bytes)

stream.stop_stream()
stream.close()

p.terminate()
