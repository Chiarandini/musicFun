# insure everything that is needed is imported
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
from audiocraft.models import MultiBandDiffusion
from ..src.classes.SignatureClass import Signature
from ..src.classes.AudioClass import Audio
from pydub import AudioSegment
import numpy as np
import gc
import torch
# import torchaudio
# import torchaudio
# from pydub.utils import mediainfo


class Ai(object):
    duration = 10
    model_type = 'melody'
    model = musicgen.MusicGen.get_pretrained('melody', device='cuda')
    model.set_generation_params(duration=duration)
    mbd = MultiBandDiffusion.get_mbd_musicgen()

    @staticmethod
    def CreateSignature(audio: Audio, description: list[str]) -> AudioSegment:
        melody_waveform = torch.from_numpy(np.array(audio.raw_audio.get_array_of_samples()))
        sr = audio.raw_audio.frame_rate
        melody_waveform = melody_waveform.unsqueeze(0).repeat(len(description), 1, 1)
        output = Ai.model.generate_with_chroma(
            descriptions=description,
            melody_wavs=melody_waveform,
            melody_sample_rate=sr,
            progress=True, return_tokens=True
        )
        # display_audio(output[0], sample_rate=32000)
        out_diffusion = Ai.mbd.tokens_to_wav(output[1])
        # display_audio(out_diffusion, sample_rate=32000)

        # memory is an issue
        gc.collect()
        torch.cuda.empty_cache()
        return out_diffusion


# 'Unique EDM Electronic',
# 'stellar EDM Electronic',
# 'magnificent EDM Electronic',
# 'awesome EDM Electronic',
# 'epic EDM Electronic',
# 'crazy EDM Electronic',
# 'EDM Electronic',
# 'superb EDM Electronic',

# melody_waveform, sr = torchaudio.load("Signature-4_016-withSilence.wav")
# print(melody_waveform)
# melody_wa
# melody_waveform = melody_waveform.unsqueeze(0).repeat(8, 1, 1)
# output = melody_model.generate_with_chroma(
#     descriptions=[
#         'Unique EDM Electronic',
#         'stellar EDM Electronic',
#         'magnificent EDM Electronic',
#         'awesome EDM Electronic',
#         'epic EDM Electronic',
#         'crazy EDM Electronic',
#         'EDM Electronic',
#         'superb EDM Electronic',
#     ],
#     melody_wavs=melody_waveform,
#     melody_sample_rate=sr,
#     progress=True, return_tokens=True
# )
# # display_audio(output[0], sample_rate=32000)
# out_diffusion = mbd.tokens_to_wav(output[1])
# display_audio(out_diffusion, sample_rate=32000)
