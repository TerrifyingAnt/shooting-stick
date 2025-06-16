from pyrogram import Client, filters
from pyrogram.types import Message


from dotenv import load_dotenv
import os

from pyrogram import Client

from openai import OpenAI
from pyrogram import Client, filters
from pyrogram.types import Message

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
token_qwen_3_test = os.getenv("TOKEN_QWEN_3_TEST")

app = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash
)

@app.on_message(filters.command("voice", prefixes=".") & filters.me)
async def send_voice(_, message):

    audio_path = "voice_module/output/brainrot.ogg"
    await app.send_voice(
        chat_id=message.chat.id,
        voice=audio_path,
    )
    await message.delete()

@app.on_message(filters.command("circle", prefixes=".") & filters.me)
async def send_circle(_, message: Message):
    video_path = "test_content/final_video_with_subtitles.mp4"  # уже сконвертированное квадратное видео
    try:
        with open(video_path, "rb") as f:
            await app.send_video_note(
                chat_id=message.chat.id,
                video_note=video_path
            )
        await message.delete()
    except Exception as e:
        await message.reply(f"❌ Ошибка при отправке кружочка: {e}")


# Конфигурация OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1/",
    api_key=token_qwen_3_test,
)

# Настраиваем системный промпт
SYSTEM_PROMPT = (
    "Ты — умный, дружелюбный AI, объясняющий вещи кратко и понятно, с примерами по необходимости."
)

@app.on_message(filters.command("askq", prefixes=".") & filters.me)
async def ask_openrouter(_, message: Message):
    user_prompt = " ".join(message.command[1:])
    if not user_prompt:
        await message.edit("❗ Введи запрос после `.askq`")
        return

    await message.edit("🧠 Думаю...")

    completion = client.chat.completions.create(
        model="qwen/qwen3-30b-a3b:free",  # или, например, "openai/gpt-4o"
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
    )
    answer = completion.choices[0].message.content
    await message.edit(answer)


app.run()
