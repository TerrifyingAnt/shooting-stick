from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from pydub import AudioSegment
import torchaudio
import torch
import scipy.io.wavfile as wavfile
import numpy as np
import os
# torch.serialization.add_safe_globals([XttsConfig])

# _original_torch_load = torch.load
# def patched_torch_load(*args, **kwargs):
#     kwargs["weights_only"] = False
#     return _original_torch_load(*args, **kwargs)

# torch.load = patched_torch_load

# Теперь можно загружать
config = XttsConfig()
config.load_json("voice_module/model/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="voice_module/model", eval=True)

brainrot_text = "Хватит лжи, и хватит боли! Бобр курва - я пердооле!!"

reference_audio = "voice_module/reference/reference_audio.wav"

outputs = model.synthesize(
    brainrot_text,
    config,
    speaker_wav=reference_audio,
    language="ru",
)

# Сохраняем WAV
wav_path = "voice_module/output/brainrot.wav"
ogg_path = "voice_module/output/brainrot.ogg"
os.makedirs(os.path.dirname(wav_path), exist_ok=True)
wavfile.write(wav_path, 24000, outputs["wav"])  # XTTS выводит 24kHz

# Загружаем WAV и конвертируем в нужный формат
audio = AudioSegment.from_wav(wav_path)
audio = audio.set_frame_rate(48000).set_channels(1)

# Экспортируем как голосовое сообщение (OGG + Opus)
audio.export(ogg_path, format="ogg", codec="libopus", bitrate="64k")

print(f"✅ Готово: {ogg_path}")