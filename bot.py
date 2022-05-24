import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from collections import Counter
import DB
from datetime import date


bot = telebot.TeleBot('5043574729:AAGJhN8IoLIkmkOciX9_0_qYUz4RMIP1gV4')
allFilms = []
allReqests = []
final = ''
def find_film(list, state):
    i = ''
    count = 0
    if state == 'year':
        num = 3
    elif state == 'name':
        num = 2
    elif state == 'time':
        num = 4
    elif state == 'director':
        num = 7
    else:
        return
    if state != 'time':
        for i in list():
            count += 1
            if i.text != '' and count == num:
                break
        return i.text
    else:
        for i in list():
            count += 1
            if i.text != '' and count == num:
                break
        return i.text


def format_time(text):
    return text[text.find('1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or '0'):]


def kino(film):
    url = "https://www.kinopoisk.ru/index.php?kp_query={}".format(film)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all('p', class_='name')[0]
    quotes = str(quotes.find('a'))[: -1]
    quotes = quotes[quotes.find('h'): quotes.rfind('>')].replace('href=', '').replace('"', '')
    return str("https://www.kinopoisk.ru/{}".format(quotes))


def oko(film):
    url = "https://www.kinopoisk.ru/index.php?kp_query={}".format(film)
    url2 = 'https://okko.tv/movie/{}'.format(film)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all('div', class_='info')[0]
    quotes = find_film(quotes, 'time')[: find_film(quotes, 'time').find(",")]
    return 'https://okko.tv/movie/{}'.format(str(quotes)).lower().replace(' ', '-')

while True:
    try:
        @bot.message_handler(commands=['start'])
        def start_message(message):
            DB.add(message.from_user.id, root=0, last_active=date.today(), name=message.from_user.username)
            bot.send_message(message.chat.id, 'Введите название фильма')


        @bot.message_handler(commands=['User'])
        def start_message(message):
            if DB.get_value('id', message.from_user.id)[5] == 1:
                bot.send_message(message.chat.id, '''Удалить пользователя: /del id
Изменить статус root: /root+ id
Получить информацию: /getinfo id''')
            else:
                bot.send_message(message.chat.id, 'Отсутствие прав доступа!')

        @bot.message_handler(commands=['del'])
        def delete(message):
            if DB.get_value('id', message.from_user.id)[5] == 1:
                if DB.get_is('id', str(message.text).replace('/del', '')):
                    DB.delete('id', str(message.text).replace('/del', ''))
                    bot.send_message(message.chat.id, 'Учетная запитсь успешно удалена!')
                else:
                    bot.send_message(message.chat.id, 'Учетная запитсь отсутствует')
            else:
                bot.send_message(message.chat.id, 'Отсутствие прав доступа!')


        @bot.message_handler(commands=['getinfo'])
        def getinfo(message):
            final = ''
            if DB.get_value('id', message.from_user.id)[5] == 1:
                if DB.get_is('id', str(message.text).replace('/getinfo', '')):
                    _ = DB.get_value('id', str(message.text).replace('/getinfo', ''))
                    bot.send_message(message.chat.id, f'''id: {_[0]}
                    
name: {_[1]}

req: {_[2]}

last_req: {_[3]}

last_active: {_[4]}

root: {_[5]}''')
                else:
                    bot.send_message(message.chat.id, 'Учетная запитсь отсутствует')
            else:
                bot.send_message(message.chat.id, 'Отсутствие прав доступа!')


        @bot.message_handler(commands=['F'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Введите найзвание фильма с приставкой /')


        @bot.message_handler(commands=['root'])
        def root_table(message):
            if DB.get_value('id', message.from_user.id)[5] == 1:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('/User', '/Stat')
                bot.send_message(message.chat.id, 'Консоль администратора:', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, 'Отсутствие прав доступа!')


        @bot.message_handler(content_types=['text'])
        def send_text(message):
            film = message.text.lower()
            DB.update_table(message.from_user.id, 'requests', DB.get_value('id', message.from_user.id)[2] + ', ' + film)
            DB.update_table(message.from_user.id, 'last_request', film)
            DB.update_table(message.from_user.id, 'last_active', date.today())
            try:
                url = "https://www.kinopoisk.ru/index.php?kp_query={}".format(film)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                quotes = soup.find_all('div', class_='info')[0]
                rating = soup.find_all('div', class_='rating')
                otvet = 'Название: ' + find_film(quotes, "name") + '\n' + 'Год: ' + find_film(quotes,
                                                                                              'year') + '\n' + \
                        'Продолжительность: ' + format_time(find_film(quotes, 'time')) + '\n' + 'Режисер: ' + \
                        find_film(quotes, 'director') + '\n' + 'Рейтинг:' + rating[0].text

                markup = types.InlineKeyboardMarkup()
                ivi = types.InlineKeyboardButton(text='ivi',
                                                 url='https://www.ivi.ru/search/?ivi_search={}'.format(film))
                url = kino(film)
                kinopoisk = types.InlineKeyboardButton(text='Кинопоиск', url=url)
                url = oko(film)
                okko = types.InlineKeyboardButton(text='Okko', url=url)
                markup.add(ivi, kinopoisk, okko)

                bot.send_message(message.chat.id, otvet, reply_markup=markup)
                allFilms.append(find_film(quotes, "name"))
                allReqests.append(film)
            except Exception as e:
                bot.send_message(message.chat.id, "Фильм не найден")
                print(e)


        bot.polling()
    except:
        pass
