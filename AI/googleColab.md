This is from the google colab:
``` python
!python3 -m pip install -U git+https://github.com/facebookresearch/audiocraft#egg=audiocraft
# !python3 -m pip install -U audiocraft

from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
import torchaudio
import gc
from audiocraft.models import MultiBandDiffusion
mbd = MultiBandDiffusion.get_mbd_musicgen()

melody_model = musicgen.MusicGen.get_pretrained('melody', device='cuda')
melody_model.set_generation_params(duration=10)


melody_waveform, sr = torchaudio.load("Signature-4_016-withSilence.wav")
melody_waveform = melody_waveform.unsqueeze(0).repeat(8, 1, 1)
output = melody_model.generate_with_chroma(
    descriptions=[
        'Unique EDM Electronic',
        'stellar EDM Electronic',
        'magnificent EDM Electronic',
        'awesome EDM Electronic',
        'epic EDM Electronic',
        'crazy EDM Electronic',
        'EDM Electronic',
        'superb EDM Electronic',
    ],
    melody_wavs=melody_waveform,
    melody_sample_rate=sr,
    progress=True, return_tokens=True
)
# display_audio(output[0], sample_rate=32000)
out_diffusion = mbd.tokens_to_wav(output[1])
display_audio(out_diffusion, sample_rate=32000)

del output
del out_diffusion
gc.collect()
torch.cuda.empty_cache()
```

This has to be put be wrapped behind a class
