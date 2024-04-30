import audiosegment as process
# from pydub import AudioSegment
from pydub.playback import play
import numpy as np
# import sys as sys
# import matplotlib.pyplot as plt

# Load the audio file
audio_file = process.from_file("signatures/Signature-4_001.mp3")

result = audio_file.filter_silence(0, 20, True)
play(result)

# print(audio_file.auditory_scene_analysis())

# Convert the audio to a numpy array
# audio_array = np.array(audio_file.get_array_of_samples())

#
# def under_zero(x: int):
#     return x < 0
#
#
# def over_zero(x: int):
#     return x > 0
#
#
# def abs_under_n(x: int, limit: int):
#     return abs(x) < limit


# thousand_range = np.fromiter((x for x in audio_array if abs_under_n(x, 1000)), dtype=audio_array.dtype)

# n, bins, patches = plt.hist(high_range)
# plt.show()

# plt.show(plt.hist(audio_array))

# convert to audio file
# thousand_range = audio_file._spawn(thousand_range)

# Calculate the Fourier transform of the audio
# fourier_transform = np.fft.fft(audio_array)

# play(thousand_range)
#

# plt.plot(audio_array)
# plt.xlabel("Frequency")
# plt.ylabel("Magnitude")
# plt.show()


# plt.plot(np.abs(fourier_transform))
