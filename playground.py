from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import sys as sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=3000)

# Load the audio file
audio_file = AudioSegment.from_mp3("signatures/Signature-4_001.mp3")

# Convert the audio to a numpy array
audio_array = np.array(audio_file.get_array_of_samples())


def under_zero(x: int):
    return x < 0
def over_zero(x: int):
    return x > 0


high_range = np.fromiter((x for x in audio_array if over_zero(x)), dtype=audio_array.dtype)

# n, bins, patches = plt.hist(high_range)
# plt.show()

# plt.show(plt.hist(audio_array))

# convert to audio file
high_range = audio_file._spawn(high_range)

# Calculate the Fourier transform of the audio
# fourier_transform = np.fft.fft(audio_array)

play(high_range)
#

plt.plot(audio_array)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.show()


# plt.plot(np.abs(fourier_transform))
