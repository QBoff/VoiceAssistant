#  Саша - голосовой помошник
# TODO
#  добавить распознование поиска погоды, распознования поиска дз, распознование
# поиска определений
#  уопределений в гугле есть общее имя класса по которому эту сноск можно
#  будет найти
#  добавить включение музыки и еще распознование
#  добавить возможность уйти в спящий режим !!!(оно наврябли нужно)!!!
# скачать word2number и deep_translator

from yandex_music import Client
import config
import stt
import tts
import datetime
from num2t4ru import num2text
import webbrowser
import random
import search_currency.search
from random import choice
import pymorphy2
import search_something.search
from sys import exit
import os
import music.music
import whatsapp_send_mes.send as wsms

morph = pymorphy2.MorphAnalyzer()

print(f"{config.VA_NAME} (v{config.VA_NAME}) начал свою работу ...")

excuses = [
    "Я не поняла что вы имеете ввиду.",
    "Что простите?",
    "Мне вас очень трудно понять.",
    "Вы говорите слишком быстро."
]


def va_respond(voice: str):
    print(voice)
    voice = voice.split(" ")
    name = ""
    tr = []
    for i in voice:
        if i in config.VA_ALIAS:
            name += i
        tr.append(i in config.VA_ALIAS)

    if any(tr):
        #  обращаются к ассистенту
        voice = " ".join(voice[voice.index(name):])

        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] == "саша":
            tts.va_speak(excuses[1])
        elif cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak(choice(excuses))
        else:
            execute_cmd(cmd)  # раньше было execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    #  for x in config.VA_TBR:
    #  cmd_split = cmd.split(" ")  # разбиваем строку на слова
    #  for word in cmd_split:
    #  if x == word:
    #  cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0, "komand": ""}
    print(cmd)
    for c, v in config.VA_CMD_LIST.items():  # заменить распознование с
        # fuzzywazzy на обычное с определение слов
        for skill in v:
            if skill in cmd or skill == cmd:
                rc['cmd'] = c
                rc['komand'] = cmd
        #  vrt = fuzz.ratio(cmd, v)
        #  if vrt > rc['percent']:
        #     rc['cmd'] = c
        #     rc['percent'] = vrt
        #     rc["komand"] = cmd
    return rc


def execute_cmd(cmd: dict):
    if cmd['cmd'] == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
    elif cmd['cmd'] == 'ctime':
        # current time
        now = datetime.datetime.now()
        hour = morph.parse("час")[0].make_agree_with_number(
            now.hour).word  # склоняем "час" с числительным колиства часов

        if now.minute >= 10:
            minute = morph.parse("минут")[0].make_agree_with_number(
                now.minute).word  # склоняем "минута" с числительным колиства
        #                         минут
        else:
            minute = morph.parse("минута")[0].make_agree_with_number(
                now.minute).word
        text = "Сейчас " + num2text(now.hour) + f" {hour} и" + " " + \
            num2text(now.minute) + f" {minute}"
        tts.va_speak(text)

    elif cmd['cmd'] == 'joke':
        joke = ""
        with open("jokes/jokes.txt", "r", encoding="utf-8") as file:
            joke = choice(file.read().split("\n"))
            while joke == " " or joke == "":
                joke = choice(file.read().split("\n"))

        tts.va_speak(joke)

    elif cmd['cmd'] == 'open_browser':
        webbrowser.open("https://www.google.com/")
        # print(cmd)

    elif cmd['cmd'] == "dollar_rate":
        val = search_currency.search.get_currency()
        text = "Курс доллара на сегодня " + num2text(val) + " рублей"
        tts.va_speak(text)

    elif cmd['cmd'] == "search":
        text_to_search = " ".join(cmd["komand"].split(" ")[1::])

        text_to_speak = search_something.search.search_req(text_to_search)
        tts.va_speak(text_to_speak)
        # webbrowser.open(f"https://www.google.com/search?q={text_to_search}")

    elif cmd['cmd'] == "weather":
        text_to_speak = search_something.search.search_weather()

        tts.va_speak(text_to_speak)

    elif cmd['cmd'] == "stop":
        exit()  # программа прекращает свою работу

    elif cmd['cmd'] == "music":
        res = music.music.play_music()
        # while True:
        #     res = music.music.play_music()
        #     sec = music.music.sec
        #     if res == "Стоп":
        #         tts.va_speak("Ваш плэйлист закончился.")
        #     elif res == "Я переключила трэк.":
        #         tts.va_speak(res)
        #         music.music.next_track()
        #         music.music.play_next_track()

        #     elif res == "Переключите трэк":
        #         tts.va_speak(res)

    elif cmd['cmd'] == "next_track":
        music.music.next_track()
        music.music.play_next_track()

    elif cmd['cmd'] == "send_message":
        # print(cmd)
        message = " ".join(cmd['komand'].split(" ")[2:-1])
        recipient = morph.parse(cmd['komand'].split(" ")[-1])[0].normal_form
        print(recipient)

        recipient = wsms.who_is_the_recipient(recipient)
        wsms.send_message(message, recipient)


#  начать прослушивание команд
stt.va_listen(va_respond)
