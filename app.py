import os
import telebot
from telebot import types
from setting import API_TOKEN
import requests
import json

###############################Global_INFO#######################

USER = {} # user_type =1 busa valunter #2 busa need

r = requests.get('https://birdamlik.uz/api/helptypes')
if r.status_code != 200:
    print("Error:", r.status_code)

data = json.loads(r.text)

HELP_TYPES = {}
DIR = os.getcwd()
i = 1
for d in data['results']:
    HELP_TYPES[i] = d
    i += 1


###############################################################

##########################Bot_setup###############################
bot = telebot.TeleBot(API_TOKEN)
#####################################################################
LANGUAGE_BUTTON_RU = "🇷🇺--Руский--🇷🇺"

LANGUAGE_BUTTON_UZ = "🇺🇿--Узбекча--🇺🇿"

VOLUNTEER_BUTTON_RU = "Волонтер"
INNEED_BUTTON_RU = "Нуждающийся"

VOLUNTEER_BUTTON_UZ = "Ёрдам олувчи"
INNEED_BUTTON_UZ = "Волонтерман"
HELP_TYPE = []


########################################################################
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/welcome_2.png', 'rb')
    bot.send_photo(chat_id, photo)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RU))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_UZ))
    bot.send_message(chat_id=chat_id,
                     text="🇺🇿--Выберите язык--🇺🇿\n 🇷🇺--Тилни танланг--🇺🇿\n 🇷🇺--Choose language--🇷🇺",
                     reply_markup=markup)


def lang_button_checker(message):
    return message.text == LANGUAGE_BUTTON_RU or message.text == LANGUAGE_BUTTON_UZ


def user_button_check(message):
    return message.text == VOLUNTEER_BUTTON_RU or message.text == INNEED_BUTTON_RU \
           or message.text == VOLUNTEER_BUTTON_UZ or message.text == INNEED_BUTTON_UZ


def user_type_set(user_type):
    if user_type == VOLUNTEER_BUTTON_RU or user_type == VOLUNTEER_BUTTON_UZ:  # or user_type == VOLUNTEER_BUTTON_EN:
        return 1
    else:
        return 2


@bot.message_handler(func=lang_button_checker)
def start_login_uzb(message):
    global USER
    chat_id = message.chat.id
    USER['chat_id'] = chat_id
    if message.text == LANGUAGE_BUTTON_RU:
        USER['lang'] = 'rus'
        photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text="\t \t \t 🙃 Нуждающийся 🙃\n или \n 😇 Волонтер 😇")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_RU))
        markup.add(types.KeyboardButton(INNEED_BUTTON_RU))
        msg = bot.send_message(chat_id=chat_id, text="выберите", reply_markup=markup)
    elif message.text == LANGUAGE_BUTTON_UZ:
        USER['lang'] = 'uzb'
        photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text="\t \t \t 🙃 Ёрдам олувчи 🙃 \n ёки \n😇 Волонтерман 😇")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_UZ))
        markup.add(types.KeyboardButton(INNEED_BUTTON_UZ))
        msg = bot.send_message(chat_id=chat_id, text="танланг", reply_markup=markup)

    bot.register_next_step_handler(msg, get_user_type)


def get_user_type(message):
    if user_button_check(message):
        global USER
        msg = message.text
        chat_id = message.chat.id
        if USER['chat_id'] == chat_id:
            USER['user_type'] = user_type_set(msg)
            if USER['user_type'] == 1:
                photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/name_1.png', 'rb')
            elif USER['user_type'] == 2:
                photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/name_2.png', 'rb')
            msg = bot.send_photo(chat_id, photo)
            bot.register_next_step_handler(msg, get_full_name)


def get_full_name(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['fullname'] = message.text
        if USER['user_type'] == 1:
            photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/phone_1.png', 'rb')
        elif USER['user_type'] == 2:
            photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/phone_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,
                                             one_time_keyboard=True)  # Подключаем клавиатуру
        if USER['lang'] == 'rus':
            button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
            lang = "Отправить телефон"
        elif USER['lang'] == 'uzb':
            button_phone = types.KeyboardButton(text="Телефон рақамингизни беринг", request_contact=True)
            lang = "Телефон рақамингизни беринг"
        # elif USER['lang'] == 'eng':
        #     button_phone = types.KeyboardButton(text="Share you cell number", request_contact=True )
        #     lang="Share you cell number"
        keyboard.add(button_phone)  # Добавляем эту кнопку
        msg = bot.send_message(chat_id, text=lang, reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_contact_info)


def make_help_button(msg):
    global HELP_TYPE
    global HELP_TYPES
    HELP_TYPE = []
    for i, j in HELP_TYPES.items():
        HELP_TYPE.append(j[msg])


def get_contact_info(message):
    global USER
    global HELP_TYPE
    lang = []
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        if message.contact != None:
            USER['PHONE'] = message.contact.phone_number
        else:
            USER['PHONE'] = message.text
        if USER['lang'] == 'uzb':
            make_help_button('title_ru')
            lang = ["ваше предложение", "ваш запрос"]
        elif USER['lang'] == 'rus':
            make_help_button('title_uz')
            lang = ["таклифингиз", "талабингиз"]
        # elif USER['lang'] == 'eng':
        #     make_help_button('title_en')
        #     lang = ["your suggestion", "you request"]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in HELP_TYPE:
            markup.add(types.KeyboardButton(i))
        # shutga next step hendler bilan qilish kere agar bir busa usertype multiple tallab biladi
        if USER['user_type'] == 1:
            photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/help_1.png', 'rb')
            bot.send_message(chat_id=chat_id, text=lang[0], reply_markup=markup)
        else:
            photo = open('/home/rakhmatjon/PycharmProjects/covid19-solidarity-tgbot/photos/help_2.png', 'rb')
            bot.send_message(chat_id=chat_id, text=lang[1], reply_markup=markup)

        print("\n\n\n")
        print(USER)
        print("\n\n\n")


if __name__ == "__main__":
    bot.polling()
