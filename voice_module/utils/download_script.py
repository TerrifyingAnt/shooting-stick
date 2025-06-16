from TTS.utils.manage import ModelManager

# Имя модели из Coqui TTS
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

# Путь куда сохранить модель
output_dir = "./xtts_v2_model"

# Создаём менеджер и скачиваем модель
manager = ModelManager()
model_path = manager.download_model(model_name)

print(f"✅ Модель успешно скачана в {model_path}")