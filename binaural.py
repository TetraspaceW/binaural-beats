import time

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5
fs = 44100
duration = 10.0

# delta - 1-4 Hz
# theta - 4-8 Hz
# alpha - 8-14 Hz
# beta - 14-30 Hz
# gamma - 30-100 Hz
# gamma / beta are where it gets interesting
beat_frequency = 30

f_left = 100.0
f_right = 100.0 + beat_frequency


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
