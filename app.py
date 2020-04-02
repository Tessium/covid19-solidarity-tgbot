import os
import telebot
from telebot import types
from setting import API_TOKEN, REGIONS
import requests
import json

###############################Global_INFO#######################

USER = {}  # user_type =1 busa valunter #2 busa need

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


def get_id_of_help_type(my_dict, val):
    for key, dic in my_dict.items():
        for k, value in dic.items():
            if val == value:
                return dic['id']


###############################################################

##########################Bot_setup###############################
bot = telebot.TeleBot(API_TOKEN)
#####################################################################
LANGUAGE_BUTTON_RU = "🇷🇺--Русcкий--🇷🇺"

LANGUAGE_BUTTON_UZ = "🇺🇿--Узбекча--🇺🇿"

VOLUNTEER_BUTTON_RU = "Волонтер"
INNEED_BUTTON_RU = "Нуждающийся"

VOLUNTEER_BUTTON_UZ = "Волонтерман"
INNEED_BUTTON_UZ = "Ёрдам олув"
HELP_TYPE = []


########################################################################
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    photo = open('photos/welcome_2.png', 'rb')
    bot.send_photo(chat_id, photo)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RU))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_UZ))
    bot.send_message(chat_id=chat_id,
                     text="🇷🇺--Выберите язык--🇷🇺\n 🇺🇿--Тилни танланг--🇺🇿",
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
        photo = open('photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_RU))
        markup.add(types.KeyboardButton(INNEED_BUTTON_RU))
        msg = bot.send_message(chat_id=chat_id, text="🙃 Нуждающийся 🙃\n или \n 😇 Волонтер 😇", reply_markup=markup)
    elif message.text == LANGUAGE_BUTTON_UZ:
        USER['lang'] = 'uzb'
        photo = open('photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_UZ))
        markup.add(types.KeyboardButton(INNEED_BUTTON_UZ))
        msg = bot.send_message(chat_id=chat_id, text="🙃 Ёрдам олувчи 🙃 \n ёки \n😇 Волонтерман 😇",
                               reply_markup=markup)

    bot.register_next_step_handler(msg, get_user_type)


def get_user_type(message):
    if user_button_check(message):
        global USER
        msg = message.text
        chat_id = message.chat.id
        if USER['chat_id'] == chat_id:
            USER['user_type'] = user_type_set(msg)
            if USER['user_type'] == 1:
                photo = open('photos/name_1.png', 'rb')
            elif USER['user_type'] == 2:
                photo = open('photos/name_2.png', 'rb')
            msg = bot.send_photo(chat_id, photo)
            lang = {
                "rus": "ФИО",
                "uzb": "ФИШ",
            }
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
            bot.register_next_step_handler(msg, get_full_name)


def get_full_name(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['full_name'] = message.text
        if USER['user_type'] == 1:
            photo = open('photos/phone_1.png', 'rb')
        elif USER['user_type'] == 2:
            photo = open('photos/phone_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,
                                             one_time_keyboard=True)  # Подключаем клавиатуру
        if USER['lang'] == 'rus':
            button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            lang = "Отправить номер телефона"
        elif USER['lang'] == 'uzb':
            button_phone = types.KeyboardButton(text="Телефон рақамингизни юборинг", request_contact=True)
            lang = "Телефон рақамингизни юборинг"
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
        if message.contact is not None:
            USER['phone'] = message.contact.phone_number
        else:
            USER['phone'] = message.text
        if USER['lang'] == 'rus':
            make_help_button('title_ru')
            lang = ["Ваше предложение", "Ваш запрос"]
        elif USER['lang'] == 'uzb':
            make_help_button('title_uz')
            lang = ["Таклифингиз", "Талабингиз"]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in HELP_TYPE:
            markup.add(types.KeyboardButton(i))
        # shutga next step handler bilan qilish kere agar bir busa usertype multiple tallab biladi
        if USER['user_type'] == 1:
            photo = open('photos/help_1.png', 'rb')
            msg = bot.send_message(chat_id=chat_id, text=lang[0], reply_markup=markup)
        else:
            photo = open('photos/help_2.png', 'rb')
            msg = bot.send_message(chat_id=chat_id, text=lang[1], reply_markup=markup)
        bot.register_next_step_handler(msg, get_help_types)


def get_help_types(message):
    global USER
    global HELP_TYPE
    lang = {
        "rus": "Достаточно",
        "uzb": "Етарлик",
    }
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        if USER['user_type'] == 1:
            if message.text != "Достаточно" and message.text != "Етарлик":
                if 'help_type' not in USER.keys():
                    USER['help_type'] = ''
                USER['help_type'] += str(get_id_of_help_type(HELP_TYPES, message.text)) + ','
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                for i in HELP_TYPE:
                    if str(get_id_of_help_type(HELP_TYPES, i)) not in USER['help_type'].split(',')[:-1]:
                        markup.add(types.KeyboardButton(i))
                markup.add(types.KeyboardButton(lang[USER["lang"]]))

                photo = open('photos/help_1.png', 'rb')
                if USER['lang'] == 'rus':
                    make_help_button('title_ru')
                    msg = bot.send_message(chat_id=chat_id, text="Еще?", reply_markup=markup)
                elif USER['lang'] == 'uzb':
                    make_help_button('title_uz')
                    msg = bot.send_message(chat_id=chat_id, text="Яна?", reply_markup=markup)
                bot.register_next_step_handler(msg, get_help_types)
            else:
                USER['help_type'] = USER['help_type'][:-1]
                lang = {
                    "rus": "Оставьте комментарий",
                    "uzb": "Изоҳ қолдиринг",
                }
                photo = open('photos/comment_1.png', 'rb')
                msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
                bot.register_next_step_handler(msg, get_comment)
        else:
            USER['help_type'] = str(get_id_of_help_type(HELP_TYPES, message.text))
            lang = {
                "rus": "Оставьте комментарий",
                "uzb": "Изоҳ қолдиринг",
            }
            photo = open('photos/comment_2.png', 'rb')
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
            bot.register_next_step_handler(msg, get_comment)


def get_comment(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['info'] = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in REGIONS.keys():
            markup.add(types.KeyboardButton(i))
        lang = {
            "rus": "Область:",
            "uzb": "Вилоят:"
        }
        if USER['user_type'] == 1:
            photo = open('photos/location_1.png', 'rb')
        elif USER['user_type'] == 2:
            photo = open('photos/location_2.png', 'rb')
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
        bot.register_next_step_handler(msg, get_region)


def get_region(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['region'] = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in REGIONS[message.text]:
            markup.add(types.KeyboardButton(i))
        lang = {
            "rus": "Район:",
            "uzb": "Туман:"
        }
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
        bot.register_next_step_handler(msg, get_city)


def get_city(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['city'] = message.text

        lang = {
            "rus": "Адрес:",
            "uzb": "Манзил:"
        }
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
        bot.register_next_step_handler(msg, get_address)


def get_address(message):
    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        USER['address'] = message.text
        photo = open('photos/ex_location_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        lang = {
            "rus": "Выберите локацию:",
            "uzb": "Аниқ манзилни танланг:"
        }
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton(text=lang[USER["lang"]], request_location=True))
        lang = {
            "rus": "Пропустить",
            "uzb": "Кейигиси"
        }
        markup.add(types.KeyboardButton(text=lang[USER["lang"]]))
        msg = bot.send_message(chat_id, text=lang[USER["lang"]], reply_markup=markup)
        bot.register_next_step_handler(msg, get_location)


def get_location(message):

    global USER
    chat_id = message.chat.id
    if USER['chat_id'] == chat_id:
        if message.text not in ["Пропустить", "Кейигиси"]:
            if message.location is not None:
                USER['location'] = str(message.location.latitude) + "," + str(message.location.longitude)
            else:
                USER['location'] = message.text
        print(USER)
        if USER['user_type'] == 1:
            r = requests.post('https://birdamlik.uz/api/volunteers/create', data=USER)
        else:
            r = requests.post('https://birdamlik.uz/api/inneed/create', data=USER)
        if r.status_code != 201:
            print("Error: ", r.status_code)
            print("Error text: ", r.text)
        else:
            lang = {
                "rus": "Успешно зарегистрирован",
                "uzb": "Муваффақиятли рўйхатдан ўтдингиз"
            }
            if USER['user_type'] == 1:
                photo = open('photos/thank_1.png', 'rb')
            else:
                photo = open('photos/thank_2.png', 'rb')
            bot.send_photo(chat_id, photo)
            bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])


if __name__ == "__main__":
    bot.polling()
