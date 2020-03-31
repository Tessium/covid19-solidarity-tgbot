from flask import Flask, request
from views import demo
import os
import telebot
from telebot import types
###############################Global_INFO#######################
USER={}
HELP_TYPES={ 1: { "id": 4,"title": "Food","title_uz": "Озиқ-овқат","title_ru": "Продукты питания","title_en": "Food"
        },
        2:{   "id": 5,"title": "Medicine","title_uz": "Дори-дармон", "title_ru": "Лекарства", "title_en": "Medicine"
        },
        3:{  "id": 6, "title": "Delivery services","title_uz": "Етказиб бериш хизмати","title_ru": "Служба доставки", "title_en": "Delivery services"
        },
        4:{ "id": 7,"title": "Masks","title_uz": "Маскалар","title_ru": "Маски","title_en": "Masks"   }}
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
HELP_TYPE=[]
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
        msg = bot.send_message(chat_id=chat_id, text="\t \t \t 🙃 Нуждающийся 🙃\n или \n 😇 Волонтер 😇")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTER_BUTTON_RUS))
        markup.add(types.KeyboardButton(NEED_BUTTON_RUS))
        msg = bot.send_message(chat_id=chat_id, text="выберите", reply_markup=markup)
    else :
        USER['lang']='uzb'
        photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text="\t \t \t 🙃 Ёрдам олувчи 🙃 \n ёки \n😇 Волонтерман 😇")
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

def make_help_button(msg):
    global HELP_TYPE
    global HELP_TYPES
    HELP_TYPE = []
    for i,j in HELP_TYPES.items():
        HELP_TYPE.append(j[msg])



def get_contact_info(message):
    global USER
    global HELP_TYPE
    lang=[]
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        if message.contact != None:
            USER['PHONE'] = message.contact.phone_number
        else:
            USER['PHONE'] = message.text
        if USER['lang'] == 'uzb':
            make_help_button('title_uz')
            lang = ["таклифингиз","талабингиз"]
        else:
            make_help_button('title_ru')
            lang = ["ваше предложение", "ваш запрос"]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in HELP_TYPE:
            markup.add(types.KeyboardButton(i))
#shutga next step hendler bilan qilish kere agar bir busa usertype multiple tallab biladi
        if USER['user_type'] ==1:
            photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\help_1.png', 'rb')
            bot.send_message(chat_id=chat_id, text=lang[0], reply_markup=markup)
        else :
            photo = open('C:\\Users\\Bokhodir\\PycharmProjects\\Birlik_covid19\\covid19-solidarity-tgbot\\photos\\help_2.png', 'rb')
            bot.send_message(chat_id=chat_id, text=lang[1], reply_markup=markup)



        print("\n\n\n")
        print(USER)
        print("\n\n\n")



if __name__ == "__main__":
   bot.polling()