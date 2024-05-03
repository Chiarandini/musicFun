import json
from classes.AudioClass import AudioSegment
from scripts.promptGenerator import response_to_prompt
from scripts.getUserInput import ask_user
from classes.SignatureClass import Audio, Signature, User
from pydub.playback import play
# from AI import AI
import os
import random
from CombineSignatureFactory import CombineSignatureFactory
from AI.AI import Ai

import copy

# 1. Connect to databases

# WARN: This is a substitute for ``connecting to the database''
with open("src/json_files/questions.json", "r") as file:
    all_questions = json.load(file)

with open("src/json_files/valid_responses.json", "r") as file:
    all_valid_responses = json.load(file)

with open("src/json_files/prompts.json", "r") as file:
    all_prompts = json.load(file)


# 2. Get prompts
responses = ask_user(all_questions, all_valid_responses)

# 3. generate prompt

ai_prompt = response_to_prompt(responses, all_prompts)
print(ai_prompt)

# 4. Pick a base signature and create audio object
# NOTE: for now this is random

base_signature_name = random.choice(os.listdir("signatures/"))  # change dir name to

print('chosen base signature: ' + base_signature_name)

# WARN: Currently, base-signatures have no descriptions
audio = Audio(AudioSegment.from_file('signatures/' + base_signature_name), '')

# 5. Use ai to get signature
# NOTE: This needs to be done on google colab atm
sig_audio = Ai.CreateSignature(audio, [ai_prompt])

# 6. Create signature object
user = User(responses)
signature1 = Signature(audio, sig_audio, user, ai_prompt)


# 7. generate another signature
# NOTE: for now just using same prompt
base_signature_name = random.choice(os.listdir("signatures/"))  # change dir name to
print('chosen base signature: ' + base_signature_name)
audio = Audio(AudioSegment.from_file('signatures/' + base_signature_name), '')
user = User(responses)
signature2 = Signature(audio, audio.raw_audio, user, ai_prompt)

# 8. create combined signature

combine_sig_factory = CombineSignatureFactory(signature1, signature2)

combined_sig = combine_sig_factory.build()


play(combined_sig.combined_signature.audio_obj.raw_audio)

# save all results to the database
# WARN: not implemented yet.
