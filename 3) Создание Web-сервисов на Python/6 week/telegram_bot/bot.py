import telebot
from telebot import types
from collections import defaultdict
from my_token import token as token_key
from telebot import apihelper
import peewee
from model import *


bot = telebot.TeleBot(token_key)
apihelper.proxy = {'https': 'socks5://127.0.0.1:9150'}

START, TITLE, LOCATION, PHOTO = range(4)
USER_STATE = defaultdict(lambda: START)
temp_data = dict()


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


# Удаление локаций
@bot.message_handler(commands=['reset'])
def reset_locations(message):
    print(message.text)
    person = Person.select().where(Person.id == message.from_user.id).get()
    locations = Location.select().where(Location.owner == person).limit(5)
    for location in locations:
        location.delete_instance()
    bot.send_message(chat_id=message.chat.id, text=f'Все места удалены')


# Вывод добавленных локаций
@bot.message_handler(commands=['list'])
def list_locations(message):
    person = Person.select().where(Person.id == message.from_user.id).get()
    locations = Location.select().where(Location.owner == person).limit(10)
    print(message.text, locations.count())
    cnt = 1
    if locations.count() > 0:
        for location in locations:
            image = open(f'{location.photo}', 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=image, caption=f'{cnt} - "{location.title}"')
            image.close()
            bot.send_location(message.chat.id, latitude=location.latitude, longitude=location.longitude)
            cnt += 1
    else:
        bot.send_message(chat_id=message.chat.id, text='У Вас нет локаций')


# Старт
@bot.message_handler(commands=['start', 'go'])
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Привет')
    update_state(message, START)


# Цепочка добавления новой локации
# Запросить название
@bot.message_handler(commands=['add'], func=lambda message: get_state(message) == START)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Укажите название')
    update_state(message, TITLE)
    # Add new user
    if Person.select().count() == 0:
        Person.create(id=message.from_user.id, state='TITLE')
    temp_data[message.from_user.id] = {'title': None, 'longitude': None, 'latitude': None, 'photo': None}


# Добавить название
@bot.message_handler(func=lambda message: get_state(message) == TITLE)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Отправьте локацию')
    update_state(message, LOCATION)
    temp_data[message.from_user.id]['title'] = message.text


# Добавить локацию
@bot.message_handler(content_types=['location'])
def add_location(message):
    bot.send_message(chat_id=message.chat.id, text=f'Отправте фото')
    temp_data[message.from_user.id]['longitude'] = message.location.longitude
    temp_data[message.from_user.id]['latitude'] = message.location.latitude
    update_state(message, PHOTO)


# Добавить фото
@bot.message_handler(content_types=['photo'], func=lambda message: get_state(message) == PHOTO)
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = './' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        update_state(message, START)
        bot.send_message(chat_id=message.chat.id, text='Локация добавлена!')
        temp_data[message.from_user.id]['photo'] = src
        add_to_db(message.from_user.id)
        print(src)
    except Exception as e:
        bot.reply_to(message, e)


def add_to_db(user_id):
    person = Person.select().where(Person.id == user_id).get()
    location = Location.create(title=temp_data[user_id]['title'],
                               longitude=temp_data[user_id]['longitude'],
                               latitude=temp_data[user_id]['latitude'],
                               photo=temp_data[user_id]['photo'],
                               owner=person)
    temp_data.pop(user_id)


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=10)
