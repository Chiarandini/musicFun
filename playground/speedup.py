from pydub import AudioSegment
from pydub import effects

root = r'audio.wav'
velocidad_X = 0.5  # speed up amount

sound = AudioSegment.from_file('./signatures/Signature-4_001.mp3')
so = sound.speedup(velocidad_X, 150, 25)
so.export(root[:-4] + 'Out.mp3', format='mp3')
