import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import pygame
from scipy.fftpack import fft

samplerate = 48000  # Get the sampling rate right: http://www.audiomountain.com/tech/audio-file-size.html
pygame.mixer.init(samplerate)

music = pygame.mixer.Sound(r"D:\Users\Charles Turvey\Music\SFX\Rising.wav")
musicarraystereo = pygame.sndarray.samples(music)
pygame.mixer.find_channel().play(pygame.sndarray.make_sound(musicarraystereo))

# Fast Fourier Transform!
T = 1 / samplerate
N = musicarraystereo.shape[0]
subN = 1000
print(N, subN, T)
x = np.float32([])  # Time
y = np.float32([])  # Frequency
z = np.float32([])  # Amplitude?
for i in range(0, N - subN):
    musicarraystereoportion = musicarraystereo[i:i + subN]
    subN = min(subN, musicarraystereoportion.shape[0])
    musicfourier = fft(musicarraystereoportion)
    freqout = np.linspace(0, 1 / (2 * T), subN // 2)
    ampout = (2 / subN) * np.abs(musicfourier[0:subN // 2])
    if ampout.shape[0] == 0:
        break
    print("%ss - %ss: Max at %s Hz (amp = %s)" % (i * T,
                                                  (i + subN) * T,
                                                  max(freqout[np.argmax(ampout, axis=0)]),
                                                  np.max(ampout)))
    x = np.append(x, (i + (subN/2)) * T)
    y = np.append(y, max(freqout[np.argmax(ampout, axis=0)]))
plt.scatter(x, y, color="#000000")
plt.show()
