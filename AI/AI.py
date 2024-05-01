# insure everything that is needed is imported
from pydub import AudioSegment
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
from signatureObjects.Signature import Signature
import torch
import numpy as np
import torchaudio
from pydub.utils import mediainfo
import gc
from audiocraft.models import MultiBandDiffusion


class AI(object):
    duration = 10
    model_type = 'melody'
    model = musicgen.MusicGen.get_pretrained('melody', device='cuda')
    model.set_generation_params(duration=duration)
    mbd = MultiBandDiffusion.get_mbd_musicgen()

    @staticmethod
    def CreateSignature(signature: Signature, description: str) -> AudioSegment:
        melody_waveform = torch.from_numpy(np.array(signature.signature.get_array_of_samples()))
        sr = signature.signature.frame_rate
        melody_waveform = melody_waveform.unsqueeze(0).repeat(1, 1, 1)
        output = AI.model.generate_with_chroma(
            descriptions=[description],
            melody_wavs=melody_waveform,
            melody_sample_rate=sr,
            progress=True, return_tokens=True
        )
        # display_audio(output[0], sample_rate=32000)
        out_diffusion = AI.mbd.tokens_to_wav(output[1])
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
