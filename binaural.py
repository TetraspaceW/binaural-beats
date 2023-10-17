import time

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 10.0  # in seconds, may be float

f_left = 100.0
f_right = 100.0 + 32  # sine frequency, Hz, may be float


def sin(freq):
    return (np.sin(2 * np.pi * np.arange(fs * duration) * freq / fs)).astype(np.float32)


placebo = False

samples_left = sin(f_left)
samples_right = sin(f_right)

if not placebo:
    samples_stereo = np.array(
        [samples_left, samples_right]
    ).T  # Combine left and right channels
    output_bytes = (volume * samples_stereo).tobytes()
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=fs, output=True)
else:
    samples_stereo = np.array(samples_left + samples_right) * 0.5
    output_bytes = (volume * samples_stereo).tobytes()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)


start_time = time.time()
stream.write(output_bytes)
stream.stop_stream()
stream.close()

p.terminate()
