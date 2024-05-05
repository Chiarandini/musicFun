# %cd musicFun/
import json
from pydub import AudioSegment
from promptGenerator import response_to_prompt
from getUserInput import ask_user
from SignatureClass import Signature
from AudioClass import Audio
from UserClass import User
from pydub.playback import play
import numpy as np
# from AI import AI
import os
import random
import torchaudio
import torch
from CombineSignatureFactory import CombineSignatureFactory
from AI import Ai
import time


from audiocraft.utils.notebook import display_audio

# 1. Connect to databases
print("1. connect to database")

# WARN: This is a substitute for ``connecting to the database''
with open("src/json_files/questions.json", "r") as file:
    all_questions = json.load(file)

with open("src/json_files/valid_responses.json", "r") as file:
    all_valid_responses = json.load(file)

with open("src/json_files/prompts.json", "r") as file:
    all_prompts = json.load(file)

print("Complete!")

# 2. Get user input
print("")
print("2. get user input")
print("**********************************************")
responses = ask_user(all_questions, all_valid_responses)
print("**********************************************")

# 3. generate prompt
print("")
print("3. generate prompt")
ai_prompt_1 = response_to_prompt(responses, all_prompts)
print(ai_prompt_1)

# 4. Pick a base signature and create audio object
print("")
print("4. pick base signature")
# NOTE: for now this is random

base_signature_name = random.choice(os.listdir("signatures/"))

print('chosen base signature: ' + base_signature_name)

# WARN: Currently, base-signatures have no descriptions
audio = Audio(AudioSegment.from_file('signatures/' + base_signature_name), '')

# 5. Use ai to get signature
print("")
print("5. create signature (using AI)")
start = time.time()
# NOTE: This needs to be done on google colab atm
sig_audio = Ai.CreateSignature(audio, [ai_prompt_1])
end = time.time()
print('took ' + str(end-start) + ' time')


# 6. Create signature object
print("")
print("6. create signature object")
user = User(responses)
signature1 = Signature(audio, sig_audio, user, ai_prompt_1)
print(signature1)


# 7. generate another signature
# NOTE: for now just using same prompt
print("")
print("7. generate another signature for combination purposes")
start = time.time()
while True:
  base_signature_name_2 = random.choice(os.listdir("signatures/"))
  if base_signature_name != base_signature_name_2:
    break
print('generate random prompt: ')
ai_prompt_2 = response_to_prompt(responses, all_prompts)
print(ai_prompt_2)

print('chosen base signature: ' + base_signature_name_2)
audio2 = Audio(AudioSegment.from_file('signatures/' + base_signature_name_2), '')
sig_audio2 = Ai.CreateSignature(audio2, [ai_prompt_2])
user = User(responses)
signature2 = Signature(audio, sig_audio2, user, ai_prompt_2)
end = time.time()
print('took ' + str(end-start) + ' time')

# 8. create combined signature
print("")
print("8. combine signatures")
start = time.time()
combine_sig_factory = CombineSignatureFactory(signature1, signature2)

combined_sig_base = combine_sig_factory.build()

combined_sig = Ai.CreateSignature(Audio(combined_sig_base.combined_signature.audio_obj.raw_audio, ''),
                                  [ai_prompt_1])

end = time.time()
print('took ' + str(end-start) + ' time')

print("**********************************************")

# print('raw signature 1:')
# raw_audio_1 =  torch.from_numpy(np.array(audio.raw_audio.get_array_of_samples())).float()

# display_audio(raw_audio_1, 32000)

print('signature 1:')
display_audio(sig_audio, 32000)

# print('raw signature 2:')
# raw_audio_2 =  torch.from_numpy(np.array(audio2.raw_audio.get_array_of_samples())).float()
# display_audio(raw_audio_2, 32000)

print('signature 2:')
display_audio(sig_audio2, 32000)

# print('raw combined signature:')
# raw_sig_base = torch.from_numpy(np.array(combined_sig_base.combined_signature.audio_obj.raw_audio.get_array_of_samples())).float()
# display_audio(raw_sig_base, 32000)

print('combined signature:')
display_audio(combined_sig, 32000)

# play(combined_sig_base.combined_signature.audio_obj.raw_audio)

# save all results to the database
# WARN: not implemented yet.
