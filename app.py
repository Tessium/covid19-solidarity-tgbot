from flask import Flask, request
from views import demo
import os
import telebot
from telebot import types
###############################USER_INFO#######################
USER={}
#user_type =1 busa valunter #2 busa need

###############################################################
##########################Bot_setup###############################
API_TOKEN = '868081058:AAFSj3Q2diNtIJnd0pt1xtC02HhhP06qxRs'
bot = telebot.TeleBot(API_TOKEN)
###################################################################
app = Flask(__name__)

app.add_url_rule('/demo',  methods=['POST', 'GET'], view_func=demo)
#####################################################################
LANGUAGE_BUTTON_RUSSIAN = "🇷🇺--Руский--🇷🇺"
LANGUAGE_BUTTON_UZBEK = "🇺🇿--УЗБЕКЧА--🇺🇿"
VOLUNTER_BUTTON_UZ = "Волонтерман"
NEED_BUTTON_UZ ="Ёрдам олувчи"
VOLUNTER_BUTTON_RUS = "Нуждающийся"
NEED_BUTTON_RUS ="Волонтер"
########################################################################
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    # path = os.path("welcome_2.png")
    # print(path)
    photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\welcome_2.png', 'rb')
    bot.send_photo(chat_id, photo)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RUSSIAN))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_UZBEK))
    bot.send_message(chat_id=chat_id, text="🇺🇿--Тилни танланг--🇺🇿\n 🇷🇺--выберите язык--🇷🇺", reply_markup=markup)

def lang_button_checker(message):
    return message.text == LANGUAGE_BUTTON_UZBEK or message.text ==LANGUAGE_BUTTON_RUSSIAN
def user_button_check(message):
    return message.text == VOLUNTER_BUTTON_UZ or message.text == NEED_BUTTON_UZ or message.text == VOLUNTER_BUTTON_RUS or message.text == NEED_BUTTON_RUS
def user_type_set(user_type):
    if user_type == VOLUNTER_BUTTON_UZ or user_type == VOLUNTER_BUTTON_RUS:
        return 1
    else:
        return 2
@bot.message_handler(func=lang_button_checker)
def start_login_uzb(message):
    global USER
    chat_id = message.chat.id
    USER['chat_id'] = chat_id
    if message.text == LANGUAGE_BUTTON_RUSSIAN :
        USER['lang']='rus'
        photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text="Нуждающийся \n Волонтер")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTER_BUTTON_RUS))
        markup.add(types.KeyboardButton(NEED_BUTTON_RUS))
        msg = bot.send_message(chat_id=chat_id, text="выберите", reply_markup=markup)
    else :
        USER['lang']='uzb'
        photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text="Ёрдам олувчи \n Волонтерман")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTER_BUTTON_UZ))
        markup.add(types.KeyboardButton(NEED_BUTTON_UZ))
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
                photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\name_1.png', 'rb')
            elif USER['user_type'] == 2:
                photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\name_2.png', 'rb')
            msg = bot.send_photo(chat_id, photo)
            bot.register_next_step_handler(msg, get_full_name)

def get_full_name(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['fullname'] = message.text
        if USER['user_type'] == 1:
            photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\phone_1.png', 'rb')
        elif USER['user_type'] == 2:
            photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\phone_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True ,one_time_keyboard=True)  # Подключаем клавиатуру
        if USER['lang'] == 'uzb':
            button_phone = types.KeyboardButton(text="Телефон рақамингизни беринг", request_contact=True )
            lang="Телефон рақамингизни беринг"
        else:
            button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
            lang = "Отправить телефон"
        keyboard.add(button_phone)  # Добавляем эту кнопку
        msg = bot.send_message(chat_id, text = lang,reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_contact_info)


def get_contact_info(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['PHONE'] = message.contact.phone_number
        print("\n\n\n")
        print(USER)
        print("\n\n\n")



if __name__ == "__main__":
   bot.polling()