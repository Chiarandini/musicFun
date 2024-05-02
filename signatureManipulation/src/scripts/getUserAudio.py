import random
from pydub import AudioSegment

file_options=['001', '002']

def get_user_audio(user_responses):
    file = 'Signature-4_001'+random.choice(file_options)+'.mp3'
    audio = AudioSegment.from_file('../../signatures/Signature-4_002.mp3')
    return audio

