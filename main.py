from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import requests
from pyrogram.types import Message

from bs4 import BeautifulSoup
from pyrogram.types import ChatPermissions
import subprocess
import time
from time import sleep
import random
import random
import asyncio

from dotenv import load_dotenv
import os


from pyrogram.raw.types import InputFile

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

# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"
    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.01) # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.01)

        except FloodWait as e:
            sleep(e.x)

R = "❤️"
W = "🤍"

chlen_list = [
    W * 9,
    W * 3 + R * 3 + W * 3,
    W * 2 + R * 5 + W * 2,
    W * 2 + R * 5 + W * 2,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 3 + R * 3 + W * 3,
    W * 2 + R * 5 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W * 9,
]


heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]

joined_heart = "\n".join(heart_list)
joined_chlen = "\n".join(chlen_list)

heartlet_len = joined_heart.count(R)
joined_chlen_len = joined_chlen.count(R)
SLEEP = 0.1


async def _wrap_edit(message: Message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x * 2)


@app.on_message(filters.command("hack", prefixes=".") & filters.me)
def hack(_, msg):
    perc = 0

    while(perc < 100):
        try:
            text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(1, 3)
            sleep(0.1)

        except FloodWait as e:
            sleep(e.x)

    msg.edit("🟢 Пентагон успешно взломан!")
    sleep(3)

    msg.edit("👽 Поиск секретных данных об НЛО ...")
    perc = 0

    while(perc < 100):
        try:
            text = "👽 Поиск секретных данных об НЛО ..." + str(perc) + "%"
            msg.edit(text)

            perc += random.randint(1, 5)
            sleep(0.15)

        except FloodWait as e:
            sleep(e.x)

    msg.edit("🦖 Найдены данные о существовании динозавров на земле!")

@app.on_message(filters.command("voice", prefixes=".") & filters.me)
async def send_voice(_, message):

    audio_path = "brainrot_reference.ogg"
    await app.send_voice(
        chat_id=message.chat.id,
        voice=audio_path,
        caption="🎤 Ваше голосовое сообщение",
        reply_to_message_id=message.id
    )
    await message.delete()

@app.on_message(filters.command("circle", prefixes=".") & filters.me)
async def send_circle(_, message: Message):
    video_path = "final_video_with_subtitles.mp4"  # уже сконвертированное квадратное видео
    try:
        with open(video_path, "rb") as f:
            await app.send_video_note(
                chat_id=message.chat.id,
                video_note=video_path,
                reply_to_message_id=message.id
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
