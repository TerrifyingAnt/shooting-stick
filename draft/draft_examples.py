import random
from time import sleep
from pyrogram.errors import FloodWait
from main import app
from pyrogram import filters

SLEEP = 0.1

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