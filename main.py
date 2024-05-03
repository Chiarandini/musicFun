import json
from pydub import AudioSegment
from promptGenerator import response_to_prompt
from getUserInput import ask_user
from SignatureClass import Signature
from AudioClass import Audio
from UserClass import User
from pydub.playback import play
# from AI import AI
import os
import random
from CombineSignatureFactory import CombineSignatureFactory
from AI import Ai

# 1. Connect to databases
print("1. connect to database")

# WARN: This is a substitute for ``connecting to the database''
with open("musicFun/src/json_files/questions.json", "r") as file:
    all_questions = json.load(file)

with open("musicFun/src/json_files/valid_responses.json", "r") as file:
    all_valid_responses = json.load(file)

with open("musicFun/src/json_files/prompts.json", "r") as file:
    all_prompts = json.load(file)


# 2. Get user input
print("2. get user input")
responses = ask_user(all_questions, all_valid_responses)

# 3. generate prompt
print("3. generate prompt")
ai_prompt = response_to_prompt(responses, all_prompts)
print(ai_prompt)

# 4. Pick a base signature and create audio object
print("4. pick base signature")
# NOTE: for now this is random

base_signature_name = random.choice(os.listdir("musicFun/signatures/"))  # change dir name to

print('chosen base signature: ' + base_signature_name)

# WARN: Currently, base-signatures have no descriptions
audio = Audio(AudioSegment.from_file('musicFun/signatures/' + base_signature_name), '')

# 5. Use ai to get signature
print("5. create signature (using AI)")
# NOTE: This needs to be done on google colab atm
sig_audio = Ai.CreateSignature(audio, [ai_prompt])

sig_audio.export('sig1.mp3', format='mp3')

# 6. Create signature object
print("6. create signature object")
user = User(responses)
signature1 = Signature(audio, sig_audio, user, ai_prompt)
print(signature1)


# 7. generate another signature
# NOTE: for now just using same prompt
print("7. generate another signature")
base_signature_name = random.choice(os.listdir("musicFun/signatures/"))  # change dir name to
print('chosen base signature: ' + base_signature_name)
audio2 = Audio(AudioSegment.from_file('musicFun/signatures/' + base_signature_name), '')
sig_audio2 = Ai.CreateSignature(audio2, [ai_prompt])
sig_audio2.export('sig2.mp3', format='mp3')
user = User(responses)
signature2 = Signature(audio, sig_audio2, user, ai_prompt)

# 8. create combined signature

print("8. combine signatures")
combine_sig_factory = CombineSignatureFactory(signature1, signature2)

combined_sig_base = combine_sig_factory.build()

combined_sig = Ai.CreateSignature(Audio(combined_sig_base.combined_signature.audio_obj.raw_audio, ''),
                                  [ai_prompt])


combined_sig.export('./result.mp3', format='mp3')

play(combined_sig_base.combined_signature.audio_obj.raw_audio)

# save all results to the database
# WARN: not implemented yet.
