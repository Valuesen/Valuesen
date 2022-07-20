# Voice Assistant v 1.4
import pyttsx3
import os
import random
import webbrowser
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
from colorama import *
from pyowm import OWM
from pyowm.utils.config import get_default_config
import datetime
import requests
from bs4 import BeautifulSoup
import sys
import wikipedia as wiki
import configparser
import re
import COVID19Py

from psutil import virtual_memory


# import alarms


class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()
    config_dict['language'] = 'ru'

    DOLLAR_GRN = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%' \
                 'B2%D0%BD%D0%B5&oq=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%' \
                 'B2%D0%BD%D0%B5&aqs=chro' \
                 'me.1.69i57j0i10i131i433j0i10l2j0i10i395l6.6599j1j7&sourceid=chrome&ie=UTF-8'

    DOLLAR_RUB = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%B' \
                 'B%D1%8E&oq=%D0%B4%D0%BE&aqs=chrome.0.69i59l2j69i57j0i395i433j0i131i395i433j69i61l3.1072j1j7&source' \
                 'id=chrome&ie=UTF-8'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.141 Safari/537.36'}

    dlrgrn = requests.get(DOLLAR_GRN, headers=headers)
    soup_grn = BeautifulSoup(dlrgrn.content, 'html.parser')
    convert_grn = soup_grn.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})

    dlrrub = requests.get(DOLLAR_RUB, headers=headers)
    soup_rub = BeautifulSoup(dlrrub.content, 'html.parser')
    convert_rub = soup_rub.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})

    ndel = ['пожалуйста', 'текущее', 'сейчас']

    commands = ['привет', 'добрый вечер', 'доброе утро', 'добрый день',
                'выключи комп', 'выруби компьютер',
                'пока',
                'покажи список команд',
                'выключи компьютер', 'выключай компьютер',
                'вырубись', 'отключись',
                'подбрось монетку', 'подкинь монетку', 'кинь монетку',
                'открой vk', 'открой браузер', 'включи vk', 'открой интернет', 'открой youtube', 'включи музон',
                'открой viber', 'включи viber', 'открывай viber',
                'найди', 'найти', 'ищи', 'кто такой',
                'как дела', 'как жизнь', 'как настроение', 'как ты',
                'открой лаунчер аризоны', 'запусти лаунчер аризоны', 'запускай лаунчер аризоны',
                'включай лаунчер аризоны', 'заходи на аризону', 'включай аризону',
                'текущее время', 'сколько времени', 'сколько время', 'сейчас времени', 'который час',
                'крути винилы', 'крути винил',
                'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
                'открой музыку', 'вруби музыку',
                'переведи',
                'планы', 'на будущее', 'что планируется',
                'открой протокол разработки', 'протокол разработки',
                'открой discord', 'запусти discord',
                'спасибо',
                'ты здесь', 'не спишь',
                'просыпайся', 'я вернулся', 'просыпайся я вернулся',
                'какой курс валют', 'скажи курс валют', 'курс валют',
                'включи балаболку', 'балаболка',
                'отбой', 'вздремни пока', 'режим ожидания', 'включи режим ожидания',
                'открой калькулятор', 'включи калькулятор',
                'найди на ютубе',
                'напомни',
                'какие обновления', 'список обновлений',
                'сколько будет',
                'какой сегодня день', 'какой сегодня месяц', 'какое сегодня число',
                'закрой протокол разработки', 'закрой протокол',
                'закрой discord', 'выключи discord',
                'выключи браузер', 'закрой браузер',
                'выключи viber', 'закрой viber',
                'включи race the sun', 'открой race the sun',
                'выключи race the sun', 'закрой race the sun',
                'открой настройки конфига', 'настройки конфига',
                'открой photoshop', 'включи photoshop', 'запусти photoshop',
                'выключи photoshop', 'закрой photoshop',
                'что идёт в кино', 'что показывают в кино', 'киносеансы',
                'расскажи анекдот', 'анекдот', 'расмеши меня',
                'открой инстаграм', 'запусти инстаграм', 'открой instagram', 'запусти instagram',
                'включи будильник', 'поставь будильник', 'разбуди меня в', 'поставь будильник на',
                'открой телеграм', 'открой telegram', 'запусти телеграм', 'запусти telegram',
                'выключи телеграм', 'выключи telegram', 'закрой телеграм', 'закрой telegram',
                'статистика заболеваемости', 'статистика коронавируса',
                'заболеваемость коронавирусом', 'какая статистика заболеваемости', ]

    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.text = ''
        self.j = 0
        self.fr = 0
        self.covid19 = COVID19Py.COVID19()
        self.task_number = 0
        wiki.set_lang('ru')
        self.cmds = {
            'выруби компьютер': self.shut, 'выключи комп': self.shut, 'выключи компьютер': self.shut,
            'выключай компьютер': self.shut,
            'подбрось монетку': self.monetka, 'подкинь монетку': self.monetka, 'кинь монетку': self.monetka,
            'найди': self.web_search, 'найти': self.web_search, 'ищи': self.web_search, 'кто такой': self.web_search,
            'что такое': self.web_search,
            'как дела': self.howyou, 'как жизнь': self.howyou, 'как настроение': self.howyou, 'как ты': self.howyou,
            'открой viber': self.viber, 'включи viber': self.viber, 'открывай viber': self.viber,
            'открой лаунчер аризоны': self.arz, 'запусти лаунчер аризоны': self.arz,
            'запускай лаунчер аризоны': self.arz,
            'включай лаунчер аризоны': self.arz, 'заходи на аризону': self.arz, 'включай аризону': self.arz,
            'пока': self.quite, 'вырубись': self.quite, 'отключись': self.quite,
            'покажи список команд': self.show_cmds,
            'открой браузер': self.brows, 'открой интернет': self.brows,
            'открой youtube': self.youtube, 'открой vk': self.ovk, 'включи vk': self.ovk,
            'открой музыку': self.music, 'включи музон': self.music, 'вруби музыку': self.music,
            'крути винилы': self.vinil, 'крути винил': self.vinil,
            'планы': self.plans, 'на будущее': self.plans, 'что планируется': self.plans,
            'переведи': self.check_translate,
            'текущее время': self.timethis, 'сейчас времени': self.timethis, 'который час': self.timethis,
            'сколько времени': self.timethis, 'сколько время': self.timethis,
            'какая погода': self.weather_pogoda, 'погода': self.weather_pogoda, 'погода на улице': self.weather_pogoda,
            'какая погода на улице': self.weather_pogoda,
            'открой протокол разработки': self.protocol, 'протокол разработки': self.protocol,
            'привет': self.hello, 'доброе утро': self.hello, 'добрый день': self.hello, 'добрый вечер': self.hello,
            'открой discord': self.discord, 'запусти discord': self.discord,
            'спасибо': self.senks,
            'ты здесь': self.youarehere, 'не спишь': self.youarehere,
            'какой курс валют': self.currency, 'скажи курс валют': self.currency, 'курс валют': self.currency,
            'включи балаболку': self.balabolka, 'балаболка': self.balabolka,
            'отбой': self.pause, 'вздремни пока': self.pause, 'режим ожидания': self.pause,
            'включи режим ожидания': self.pause,
            'открой калькулятор': self.calc, 'включи калькулятор': self.calc,
            'напомни': self.reminder,
            'какие обновления': self.updates, 'список обновлений': self.updates,
            'сколько будет': self.mathh,
            'какой сегодня день': self.days, 'какой сегодня месяц': self.days, 'какое сегодня число': self.days,
            'закрой протокол разработки': self.off_protocol, 'закрой протокол': self.off_protocol,
            'закрой discord': self.off_discord, 'выключи discord': self.off_discord,
            'выключи браузер': self.off_brows, 'закрой браузер': self.off_brows,
            'выключи viber': self.off_viber, 'закрой viber': self.off_viber,
            'включи race the sun': self.racethesun, 'открой race the sun': self.racethesun,
            'выключи race the sun': self.off_racethesun, 'закрой race the sun': self.off_racethesun,
            'открой настройки конфига': self.perezapis, 'настройки конфига': self.perezapis,
            'открой photoshop': self.photoshop, 'включи photoshop': self.photoshop, 'запусти photoshop': self.photoshop,
            'выключи photoshop': self.off_photoshop, 'закрой photoshop': self.off_photoshop,
            'что идёт в кино': self.whatinkino, 'что показывают в кино': self.whatinkino, 'киносеансы': self.whatinkino,
            'расскажи анекдот': self.anekdot, 'анекдот': self.anekdot, 'расмеши меня': self.anekdot,
            'открой инстаграм': self.insta, 'запусти инстаграм': self.insta, 'открой instagram': self.insta,
            'запусти instagram': self.insta,
            'включи будильник': self.alarmer, 'поставь будильник': self.alarmer, 'разбуди меня в': self.alarmer,
            'поставь будильник на': self.alarmer,
            'открой телеграм': self.opentg, 'открой telegram': self.opentg, 'запусти телеграм': self.opentg,
            'запусти telegram': self.opentg,
            'выключи телеграм': self.off_tg, 'выключи telegram': self.off_tg, 'закрой телеграм': self.off_tg,
            'закрой telegram': self.off_tg,
            'статистика заболеваемости': self.covid_stat, 'статистика коронавируса': self.covid_stat,
            'заболеваемость коронавирусом': self.covid_stat, 'какая статистика заболеваемости': self.covid_stat,
        }

    def is_not_used(self):
        pass

    def plans(self):
        self.talk('Моя задача будет заключаться в помощи в управлении компьютером'
                  'На данный момент ведется работа над виртуальной частью программного обеспечения'
                  'Так же ведется работа по оптимизации всех существующих в коде функций'
                  'В будущем в планах написать систему распознавания лица'
                  'И сделать уровни допуска к командам'
                  'В конечном итоге моя цель будет достигнута')

    def comparison(self, x):  # осуществляет поиск самой подходящей под запрос функции
        commands = Assistant.commands
        ans = ''
        for i in range(len(commands)):
            k = fuzz.ratio(x, commands[i])
            if (k > 70) & (k > self.j):
                ans = commands[i]
                self.j = k
        return str(ans)

    def show_cmds(self):  # выводит на экран список доступных комманд
        self.is_not_used()
        for i in Assistant.commands:
            print(i)
        time.sleep(1)

    def anekdot(self):
        s = requests.get('http://anekdotme.ru/random')
        b = BeautifulSoup(s.text, "html.parser")
        p = b.select('.anekdot_text')
        s = (p[0].getText().strip())
        reg = re.compile('[^a-zA-Zа-яА-я ^0-1-2-3-4-5-6-7-8-9.,!?-]')
        s = reg.sub('', s)
        self.talk(s)

    def protocol(self):
        self.talk('Протокол разработки открыт')
        os.startfile('C:/Users/Ruslan/PycharmProjects/Voice_Assistant/protocol.txt')

    def web_search_yt(self):
        k = ['Вот что я нашла по вашему запросу', 'Вот что мне удалось найти', 'Вот что я нашла']
        tr = 0
        variants = ['найди на ютубе', 'поиск на ютубе']
        for i in variants:
            if (i in self.text) & (tr == 0):
                repl = self.text
                repl = repl.replace('найди на ютубе', '').strip()
                repl = repl.replace('поиск на ютубе', '').strip()
                self.talk(random.choice(k))
                webbrowser.open(f'https://www.youtube.com/results?search_query={repl}')
                tr = 0
                self.text = ''

    def covid_stat(self):
        URL = 'https://ncov.blog/countries/ru/77/'
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203 (Edition Yx 08) '
        }
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('div', 'card-text pt-3')
        weather = items[0].find('span', 'badge-pill p-2 badge-light').text.replace("+", '')
        self.talk('Сегодня в москве заболело ' + weather[0] + ' тысяч ' + weather[2:5] + ' человека')

    def updates(self):
        self.is_not_used()
        print('Список обновлений версии 1.4')
        print('Версия была переписана под ООП')
        print('Добавлена функция вычисления процента от числа')
        print('Исправлен баг в функции quite')
        print('Исправлен баг в функции hello')
        print('Добавлена функция "Какой сегодня день"')
        print('Была доработана функция "Какой сегодня день"')
        print('Метод self.engine.say был заменен функцией self.talk()')
        print('Была сделана функция выключения браузера, дискорда, вайбера и протокола разработки)')
        print('Была добавлена википедия для web_search')
        print('Был сделан конфиг с основными переменными данных (place, country)')
        print('Был добавлен новый саундтрек в функцию music')
        print('Была сделана функция показа расписания в ближайших кинотеатрах')
        print('Добавлена функция "Расскажи анекдот"')
        print('Добавлена команда открытия инстаграма')
        print('Полностью вырезана функция web_search_yt')
        print('Обновлён Плейлист с музыкой')
        print('Добавлена команда открытия Телеграмма')

    def mathh(self):
        if fuzz.ratio(self.text, 'сколько будет') > 50:
            zapros = self.text.replace('сколько будет', '').strip()
            zpr = (f'https://www.google.com/search?q={zapros}&oq={zapros}'
                   f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
            zapr1 = requests.get(zpr, headers=Assistant.headers)
            soup_zap = BeautifulSoup(zapr1.content, 'html.parser')
            res = soup_zap.findAll("span", {"class": "qv3Wpe"})
            self.talk(zapros + ' будет' + res[0].text)
            self.text = ''

    def whatinkino(self):
        k = ["Вот что я нашла по вашему запросу", "Открываю расписание кинотеатров", "Вот что я нашла"]
        self.talk(random.choice(k))
        webbrowser.open('https://yandex.ru/search/?text=кино&lr=213')

    def photoshop(self):
        try:
            k = ["Запускаю фотошоп", "Открываю фотошоп"]
            os.startfile("G:\\Neor Gaming v2.0\\Photoshop\\Photoshop.exe")
            self.talk(random.choice(k))
        except OSError:
            self.talk('Операция была отменена')

    def web_search(self):
        tr = 0
        k = ['Вот что я нашла по вашему запросу', 'Вот что мне удалось найти', 'Вот что я нашла']
        variants = ['найди', 'что такое', 'кто такой', 'найти', 'ищи']
        for i in variants:
            if (i in self.text) & (tr == 0):
                repl = self.text
                repl = repl.replace(i, '').strip()
                self.talk(random.choice(k))
                webbrowser.open(f'https://www.google.com/search?q={repl}&oq={repl}'
                                f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
                try:
                    info = wiki.summary(repl)
                    self.talk(((info[0:230]).replace('англ', '')).replace('род.', 'родился').replace('(.', '')
                              .replace(')', '').replace(';', ''))
                except wiki.exceptions.PageError:
                    pass
                except wiki.exceptions.WikipediaException:
                    pass
                del repl
                tr = 0
                self.text = ''

    def vinil(self):
        self.is_not_used()
        webbrowser.open('https://www.youtube.com/watch?v=zqY-Wr43j94&t=0s')

    def racethesun(self):
        k = ["Запускаю Race The Sun", "Включаю Race The Sun"]
        self.talk(random.choice(k))
        os.startfile('G://games//Race The Sun v1.531//RaceTheSun.exe')

    def off_racethesun(self):
        k = ["Выключаю Race The Sun", "Race The Sun выключен"]
        self.talk(random.choice(k))
        os.system('taskkill /IM "RaceTheSun.exe" /F')

    def insta(self):
        k = ["Открываю Инстаграм", "Запускаю Инстаграм"]
        self.talk(random.choice(k))
        webbrowser.open("https://instagram.com/")

    def balabolka(self):
        num = 1
        while num == 1:
            k = input("Введите текст который надо озвучить: ")
            self.talk(k)
            num = num + 1

    def monetka(self):
        self.talk("Подбрасываю...")
        k = ["Выпал Орёл", "Выпала Решка"]
        self.talk(random.choice(k))

    def youarehere(self):
        k = ['Слушаю вас', 'К вашим услугам']
        self.talk(random.choice(k))

    def senks(self):
        k = ['Обращайтесь', 'Всегда рада помочь', 'Не за что!']
        self.talk(random.choice(k))

    def clear_task(self):  # удаляет ключевые слова
        for z in Assistant.ndel:
            self.text = self.text.replace(z, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

    def hello(self):
        now = datetime.datetime.now()
        # print(hour.hour)
        # print(int(hour.hour))
        if int(now.hour) >= 6 and now.hour < 12:
            z = ["Доброе утро, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.talk(random.choice(z))
        elif int(now.hour) >= 12 and now.hour < 18:
            z = ["Добрый день, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.talk(random.choice(z))
        elif int(now.hour) >= 18 and now.hour < 23:
            z = ["Добрый вечер, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.talk(random.choice(z))
        else:
            z = ["Доброй ночи, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.talk(random.choice(z))

    def viber(self):
        self.is_not_used()
        os.startfile("C:/Users/Ruslan/AppData/Local/Viber/Viber.exe")

    def quite(self):  # функция выхода из программы
        x = ['Надеюсь мы скоро увидимся!', 'Рада была помочь', 'Я отключаюсь']
        self.talk(random.choice(x))
        self.engine.stop()
        os.system('cls')
        sys.exit(0)

    def cfile(self):
        if self.fr == 0:
            self.is_not_used()
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nbrowser = chrome\nfcreated = 1')
            file.close()
            self.fr += 1

    def perezapis(self):
        self.is_not_used()
        onoff = 1
        self.talk("Введите номер переменной которую вы хотите изменить")
        while onoff == 1:
            numb = input(("Изменить город '1'\nИзменить страну '2'\nИзменить браузер '3'"
                          "\nВыключить режим редактирования данных '0'"
                          "\nВведите номер переменной в которой хотите изменить значение: "))
            if str(numb) == "1":
                with open('settings.ini', 'r') as f:
                    old = f.read()
                nplace = Assistant.settings['SETTINGS']['place']
                cnew = input("Введите город (Пример Kharkov): ")
                new = old.replace(nplace, cnew)
                with open('settings.ini', 'w') as f:
                    f.write(new)
                print("Город успешно изменён!")
            elif str(numb) == "2":
                with open('settings.ini', 'r') as f:
                    old = f.read()
                ncountry = Assistant.settings['SETTINGS']['country']
                cnew = input("Введите код страны (Пример UA): ")
                new = old.replace(ncountry, cnew)
                with open('settings.ini', 'w') as f:
                    f.write(new)
                print("Страна успешно изменена")
            elif str(numb) == "3":
                with open('settings.ini', 'r') as f:
                    old = f.read()
                nbrows = Assistant.settings['SETTINGS']['browser']
                cnew = input("Введите название браузера (Например chrome, firefox, opera): ")
                new = old.replace(nbrows, cnew)
                with open('settings.ini', 'w') as f:
                    f.write(new)
                print("Браузер успешно изменён")
            elif str(numb) == "0":
                print("Режим редактирования выключен")
                onoff = onoff + 1

    def weather_pogoda(self):
        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']
        country_and_place = place + ", " + country
        owm = OWM('fd5321547e631b45b33d6d1cc673754f')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        w = observation.weather
        status = w.detailed_status
        w.wind()
        temp = w.temperature('celsius')['temp']
        URL = 'https://yandex.ru/pogoda/213?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content' \
              '=wizard_desktop_main&utm_term=title '
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203 (Edition Yx 08) '
        }
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items2 = soup.findAll('div', 'maps-widget-fact maps-widget-nowcast__inner')
        weather = items2[0].find('p', 'maps-widget-fact__title').text

        if weather == 'Открыть карту осадков':
            self.talk("В городе Москва сейчас " + str(status) + '. Температура воздуха составляет ' + str(
                round(temp)) + ' ° .')
        else:
            self.talk("В городе Москва сейчас " + str(status) + '. Температура воздуха составляет ' + str(
                round(temp)) + ' ° . ' + weather + ' . ')

        if int(temp) <= -19 + 4:
            self.talk("На улице очень сильно холодно, одевайте термобельё и постарайтесь поменьше "
                      "находиться на улице, не забудьте про тёплые перчатки")
        elif int(temp) <= -15 + 4:
            self.talk("Сегодня на улице достаточно холодно, одевайтесь теплее и не забудьте взять перчатки")
        elif int(temp) <= -10 + 4:
            self.talk("Сегодня холодно, одевайте зимнюю куртку и шапку, так-же не забудьте взять с собой перчатки")
        elif int(temp) <= -5 + 4:
            self.talk("Сегодня относительно прохладно, одевайте теплую куртку и пальто")
        elif int(temp) <= 0 + 4:
            self.talk("Сегодня прохладно, рекомендую одевать пальто")
        elif int(temp) <= 5 + 4:
            self.talk("Сегодня на улице прохладно одевайте куртку или плащ")
        elif int(temp) <= 10 + 4:
            self.talk("На улице прохладно, рекомендую одеваться лёгко, одевайте штаны и ветровку")
        elif int(temp) <= 15 + 4:
            self.talk("На улице достаточно тепло, но рекомендую одеть ветровку")
        elif int(temp) <= 20 + 4:
            self.talk("Сегодня очень тепло, одевайте шорты и футболку")
        elif int(temp) <= 21 + 999:
            self.talk("Сегодня жарко, одевайте шорты и футболку")
        else:
            pass
        if str(status) == "дождь":
            self.talk("Не забудьте взять с собой зонтик")

    def brows(self):  # открывает браузер
        webbrowser.open('https://yandex.ru')
        self.talk("Браузер открыт!")

    def opentg(self):
        os.startfile(r"C:\Users\ВП\Desktop\Telegram.lnk")
        self.talk('Открываю Телеграм')

    def pause(self):
        num = 1
        m = ['Переключаюсь в режим ожидания', 'Если буду нужна, обращайтесь']
        self.talk(random.choice(m))
        while num == 1:
            self.engine.runAndWait()
            self.text = self.listen()
            if (fuzz.ratio(self.text, 'просыпайся') > 60) or (fuzz.ratio(self.text, "проснись") > 60
                                                              or (fuzz.ratio(self.text, "просыпайся я вернулся") > 60)):
                k = ['Что вам угодно?', 'Я вас слушаю', 'Чем могу быть полезна?', 'Чем вам помочь?',
                     'К вашим услугам']
                self.talk(random.choice(k))
                num = num + 1

    def reminder(self):
        remind = str(input("Что мне вам напомнить? "))
        local_time = float(input("Через сколько минут? "))
        local_time = local_time * 60
        time.sleep(local_time)
        self.talk(remind)
        print(remind)

    def off_protocol(self):
        os.system('taskkill /IM "notepad.exe" /F')
        os.system('cls')
        k = ['Протокол разработки закрыт', 'Закрываю Протокол разработки']
        self.talk(random.choice(k))

    def off_tg(self):
        os.system('taskkill /IM "Telegram.exe" /F')
        os.system('cls')
        k = ['Телеграм закрыт', 'Закрываю Телеграм']
        self.talk(random.choice(k))

    def off_discord(self):
        os.system('taskkill /IM "discord.exe" /F')
        os.system('cls')
        k = ['Выключаю Дискорд', 'Закрываю Дискорд', 'Discord Дискорд']
        self.talk(random.choice(k))

    def off_photoshop(self):
        os.system('taskkill /IM "Photoshop.exe" /F')
        os.system('taskkill /IM "CS6ServiceManager.exe" /F')
        # os.system('cls')
        k = ['Выключаю Фотошоп', 'Закрываю Фотошоп', 'Фотошоп закрыт']
        self.talk(random.choice(k))

    def off_brows(self):
        browser = Assistant.settings['SETTINGS']['browser']
        sbrows = browser + ".exe"
        os.system(f'taskkill /IM {sbrows} /F')
        os.system('cls')
        k = ['Браузер закрыт', 'Закрываю браузер']
        self.talk(random.choice(k))

    def off_viber(self):
        os.system('taskkill /IM "Viber.exe" /F')
        os.system('cls')
        k = ['Закрываю Viber', 'Viber закрыт']
        self.talk(random.choice(k))

    def currency(self):
        self.talk("Желаете что-бы я озвучила курс или вывела его?")
        self.text = self.listen()
        print(self.text)
        if (fuzz.ratio(self.text, 'озвучь') > 80) or (fuzz.ratio(self.text, "скажи") > 80):
            self.talk("Курс одного доллара составляет " + Assistant.convert_rub[0].text + "рубля")
        else:
            self.talk('Курс выведен на экран')
            print("Курс 1 доллара составляет: " + Assistant.convert_rub[0].text + " рубля")

    def howyou(self):
        k = ["Всегда готова к работе!", "Отлично!", "Вполне сносно"]
        self.talk(random.choice(k))

    def discord(self):
        self.is_not_used()
        os.system(r'C:\Users\ВП\Desktop\развлечения\Discord.lnk')
        os.system('cls')

    def calc(self):
        self.talk('Открываю калькулятор')
        os.system('calc')

    def arz(self):
        self.talk("Аризона лаунчер открыт")
        os.startfile('G:/games/ARIZONA GAMES/arizona-starter.exe')

    def ovk(self):  # открывает вк
        self.talk("Вконтакте открыто")
        webbrowser.open('https://vk.com/feed')

    def youtube(self):  # открывает ютюб
        self.talk("Youtube открыт")
        webbrowser.open('https://www.youtube.com')

    def days(self):
        now = datetime.datetime.now()
        month = ''
        day = ''
        if now.month == 1:
            month = 'Января'
        elif now.month == 2:
            month = 'Февраля'
        elif now.month == 3:
            month = 'Марта'
        elif now.month == 4:
            month = 'Апреля'
        elif now.month == 5:
            month = 'Мая'
        elif now.month == 6:
            month = 'Июня'
        elif now.month == 7:
            month = 'Июля'
        elif now.month == 8:
            month = 'Августа'
        elif now.month == 9:
            month = 'Сентября'
        elif now.month == 10:
            month = 'Октября'
        elif now.month == 11:
            month = 'Ноября'
        elif now.month == 12:
            month = 'Декабря'
        if now.day == 1:
            day = 'Первое'
        if now.day == 2:
            day = 'Второе'
        if now.day == 3:
            day = 'Третье'
        if now.day == 4:
            day = 'Четвётое'
        if now.day == 5:
            day = 'Пятое'
        if now.day == 6:
            day = 'Шестое'
        if now.day == 7:
            day = 'Седьмое'
        if now.day == 8:
            day = 'Восьмое'
        if now.day == 9:
            day = 'Девятое'
        if now.day == 10:
            day = 'Десятое'
        if now.day == 11:
            day = 'Одиннадцатое'
        if now.day == 12:
            day = 'Двенадцатое'
        if now.day == 13:
            day = 'Тринадцатое'
        if now.day == 14:
            day = 'Четырнадцатое'
        if now.day == 15:
            day = 'Пятнадцатое'
        if now.day == 16:
            day = 'Шестнадцатое'
        if now.day == 17:
            day = 'Семнадцатое'
        if now.day == 18:
            day = 'Восемнадцатое'
        if now.day == 19:
            day = 'Девятнадцатое'
        if now.day == 20:
            day = 'Двадцатое'
        if now.day == 21:
            day = 'Двадцать первое'
        if now.day == 22:
            day = 'Двадцать второе'
        if now.day == 23:
            day = 'Двадцать третье'
        if now.day == 24:
            day = 'Двадцать четвёртое'
        if now.day == 25:
            day = 'Двадцать пятое'
        if now.day == 26:
            day = 'Двадцать шестое'
        if now.day == 27:
            day = 'Двадцать седьмое'
        if now.day == 28:
            day = 'Двадцать восьмое'
        if now.day == 29:
            day = 'Двадцать девятое'
        if now.day == 30:
            day = 'Тридцатое'
        if now.day == 31:
            day = 'Тридцать первое'
        self.talk('Сегодня ' + str(day) + ' ' + str(month))

    def timethis(self):  # время
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def shut(self):  # выключает компьютер
        self.talk("Подтвердите действие!")
        self.text = self.listen()
        print(self.text)
        if (fuzz.ratio(self.text, 'подтвердить') > 60) or (fuzz.ratio(self.text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            os.system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(self.text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")

    def music(self):
        self.is_not_used()
        k = ['https://www.youtube.com/watch?v=UkSr9Lw5Gm8&t=0s', 'https://www.youtube.com/watch?v=YlsQ6hjSZ8A&t=0s',
             'https://www.youtube.com/watch?v=bcyvZIoQp9A&t=0s', 'https://www.youtube.com/watch?v=eQxmhqaR2OA&t=0s',
             'https://www.youtube.com/watch?v=5TZYXG6Asj4A&t=0s', 'https://www.youtube.com/watch?v=Kt-tLuszKBA&t=0s', ]
        webbrowser.open(random.choice(k))

    def alarmer(self):
        tr = 0
        variants = ['включи будильник', 'поставь будильник', 'разбуди', 'меня', 'в', 'на', ]
        for i in variants:
            if (i in self.text) & (tr == 0):
                timetoalarm = self.text
                timetoalarm = timetoalarm.replace('включи будильник', '').strip()
                timetoalarm = timetoalarm.replace('поставь будильник', '').strip()
                timetoalarm = timetoalarm.replace('разбуди', '').strip()
                timetoalarm = timetoalarm.replace('в', '').strip()
                timetoalarm = timetoalarm.replace('на', '').strip()
                timetoalarm = timetoalarm.replace('меня', '').strip()
                self.talk("Будильник поставлен на " + timetoalarm)
                # alarms.alarms(timetoalarm)
                tr = 1
                self.text = ''

    def check_translate(self):
        tr = 0
        variants = ['переведи', 'перевести', 'переводить', 'перевод']
        for i in variants:
            if (i in self.text) & (tr == 0):
                word = self.text
                word = word.replace('переведи', '').strip()
                word = word.replace('перевести', '').strip()
                word = word.replace('переводить', '').strip()
                word = word.replace('перевод', '').strip()
                word = word.replace('слово', '').strip()
                word = word.replace('слова', '').strip()
                webbrowser.open('https://translate.google.ru/#view=home&op=translate&sl=auto&tl=ru&text={}'.format(word)
                                )
                tr = 1
                self.text = ''

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        self.text = ''
        with sr.Microphone() as sourse:
            print('Я вас слушаю: ')
            self.r.adjust_for_ambient_noise(sourse)
            audio = self.r.listen(sourse, phrase_time_limit=3)  # phrase_time_limit=3
            try:
                self.text = (self.r.recognize_google(audio, language="ru-RU")).lower()
            except sr.UnknownValueError:
                pass
            except TypeError:
                pass
            os.system('cls')
            # print(self.text)
            self.clear_task()
            return self.text

    def cmd_exe(self):
        self.check_translate()
        self.web_search()
        self.mathh()
        # self.alarmer()
        self.text = self.comparison(self.text)
        print(self.text)
        if self.text in self.cmds:
            if (self.text != 'пока') & (self.text != 'покажи список команд') \
                    & (self.text != 'текущее время') & (self.text != 'сколько времени') \
                    & (self.text != 'сколько время') & (self.text != 'сейчас времени') & (self.text != 'который час') \
                    & (self.text != 'планы') & (self.text != 'какая погода') \
                    & (self.text != 'привет') & (self.text != 'доброе утро') & (self.text != 'добрый день') \
                    & (self.text != 'добрый вечер') \
                    & (self.text != 'как дела') & (self.text != 'как жизнь') & (self.text != 'как настроение') \
                    & (self.text != 'как ты') \
                    & (self.text != 'погода') & (self.text != 'погода на улице') \
                    & (self.text != 'какая погода на улице') \
                    & (self.text != 'выруби компьютер') & (self.text != 'выключи комп') \
                    & (self.text != 'выключи компьютер') \
                    & (self.text != 'выключи компьютер') & (self.text != 'выключай компьютер') \
                    & (self.text != 'спасибо') \
                    & (self.text != 'открой калькулятор') & (self.text != 'включи калькулятор') \
                    & (self.text != 'ты здесь') & (self.text != 'не спишь') \
                    & (self.text != 'какой курс валют') & (self.text != 'скажи курс валют') \
                    & (self.text != 'курс валют') \
                    & (self.text != 'какой сегодня день') & (self.text != 'какой сегодня месяц') \
                    & (self.text != 'какое сегодня число') \
                    & (self.text != 'включи балаболку') & (self.text != 'балаболка') \
                    & (self.text != 'расскажи анекдот') & (self.text != 'анекдот') & (self.text != 'расмеши меня') \
                    & (self.text != 'что идёт в кино') & (self.text != 'что показывают в кино') \
                    & (self.text != 'киносеансы') \
                    & (self.text != 'отбой'):
                k = ['Секундочку', 'Сейчас сделаю', 'Уже выполняю']
                self.talk(random.choice(k))
            self.cmds[self.text]()
        elif self.text == '':
            pass
        else:
            print('Команда не найдена!')
        self.task_number += 1
        if self.task_number % 10 == 0:
            self.talk('У вас будут еще задания?')
        self.engine.runAndWait()
        self.engine.stop()

    # исправляет цвет

    print(Fore.YELLOW + '', end='')
    os.system('cls')

    def main(self):
        fr = 0
        try:
            fcr = Assistant.settings['SETTINGS']['fcreated']
            if int(fcr) != 1:
                if fr == 0:
                    self.cfile()
                    fr += 1
        except KeyError:
            print("Файл settings.ini был создан!")
            self.talk("Для настройки конфигурации скажите 'Открой настройки конфига' ")
            fr += 1
            self.cfile()
        try:
            self.listen()
            if self.text != '':
                self.cmd_exe()
                self.j = 0
        except UnboundLocalError:
            pass
        except NameError:
            pass
        except TypeError:
            pass
        except IndentationError:
            pass
        except IndexError:
            pass
        except ValueError:
            pass
        except KeyError:
            pass
        except NotImplementedError:
            pass
        except SyntaxError:
            pass
        except AttributeError:
            pass


while True:
    Assistant().main()
