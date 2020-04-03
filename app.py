import os
import telebot
from telebot import types
from setting import API_TOKEN, REGIONS
import requests
import json

###############################Global_INFO#######################

USERS = []

r = requests.get('https://api.birdamlik.uz/api/helptypes')
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
LANGUAGES = [LANGUAGE_BUTTON_RU, LANGUAGE_BUTTON_UZ]

VOLUNTEER_BUTTON_RU = "Я волонтер"
INNEED_BUTTON_RU = "Я нуждающийся"

VOLUNTEER_BUTTON_UZ = "Волонтерман"
INNEED_BUTTON_UZ = "Ёрдам олувчиман"
TYPES = {
    "uzb": [VOLUNTEER_BUTTON_UZ, INNEED_BUTTON_UZ, ],
    "rus": [VOLUNTEER_BUTTON_RU, INNEED_BUTTON_RU]
}

HELP_TYPE = []


########################################################################
def restart_btn_checker(message):
    return message.text == 'Начать сначала' or message.text == 'Бошидан бошлаш'


@bot.message_handler(commands=['start'])
@bot.message_handler(func=restart_btn_checker)
def start(message):
    global USERS
    chat_id = message.chat.id
    for i in USERS:
        if i['chat_id'] == chat_id:
            USERS.remove(i)
    photo = open('photos/welcome_2.png', 'rb')
    bot.send_photo(chat_id, photo)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RU))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_UZ))
    msg = bot.send_message(chat_id=chat_id,
                           text="🇷🇺--Выберите язык--🇷🇺\n 🇺🇿--Тилни танланг--🇺🇿",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, start_login_uzb)


def user_button_check(message):
    return message.text == VOLUNTEER_BUTTON_RU or message.text == INNEED_BUTTON_RU \
           or message.text == VOLUNTEER_BUTTON_UZ or message.text == INNEED_BUTTON_UZ


def user_type_set(user_type):
    if user_type == VOLUNTEER_BUTTON_RU or user_type == VOLUNTEER_BUTTON_UZ:
        return 1
    else:
        return 2


def start_login_uzb(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    USER['chat_id'] = chat_id

    if message.text == LANGUAGE_BUTTON_RU:
        USER['lang'] = 'rus'
        USERS.append(USER)
        photo = open('photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_RU))
        markup.add(types.KeyboardButton(INNEED_BUTTON_RU))
        msg = bot.send_message(chat_id=chat_id, text=f'__Нуждающийся__ или __Волонтер__', parse_mode='Markdown',
                               reply_markup=markup)
    elif message.text == LANGUAGE_BUTTON_UZ:
        USER['lang'] = 'uzb'
        USERS.append(USER)
        photo = open('photos/profile_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton(VOLUNTEER_BUTTON_UZ))
        markup.add(types.KeyboardButton(INNEED_BUTTON_UZ))
        msg = bot.send_message(chat_id=chat_id, text=f'__Ёрдам олувчи__ ёки __Волонтер__', parse_mode='Markdown',
                               reply_markup=markup)
    else:
        lang = {
            "rus": "Пожалуйста, выберите из списка:",
            "uzb": "Илтимос, руйхатдан танланг:"
        }
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in LANGUAGES:
            markup.add(types.KeyboardButton(i))
        msg = bot.send_message(chat_id=chat_id, text=lang["rus"] + "\n" + lang["uzb"], reply_markup=markup)
        bot.register_next_step_handler(msg, start_login_uzb)
        return
    bot.register_next_step_handler(msg, get_user_type)


def get_user_type(message):
    global USERS
    msg = message.text
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if user_button_check(message):
        if USER['chat_id'] == chat_id:
            USER['user_type'] = user_type_set(msg)
            if USER['user_type'] == 1:
                photo = open('photos/name_1.png', 'rb')
            elif USER['user_type'] == 2:
                photo = open('photos/name_2.png', 'rb')
            msg = bot.send_photo(chat_id, photo)
            lang = {
                "rus": "Ф.И.О:",
                "uzb": "Ф.И.Ш:",
            }
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
            bot.register_next_step_handler(msg, get_full_name)
    else:
        lang = {
            "rus": "Пожалуйста, выберите из списка:",
            "uzb": "Илтимос, руйхатдан танланг:"
        }
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in TYPES[USER["lang"]]:
            markup.add(types.KeyboardButton(i))
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
        bot.register_next_step_handler(msg, start_login_uzb)
        return


def get_full_name(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
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
            lang = "Отправьте номер телефона"
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
    global USERS
    global HELP_TYPE
    lang = []
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        if message.contact is not None:
            USER['phone'] = message.contact.phone_number
        else:
            USER['phone'] = message.text
        if USER['lang'] == 'rus':
            make_help_button('title_ru')
            lang = ["Как вы можете помочь?", "Какая помощь вам нужна?"]
        elif USER['lang'] == 'uzb':
            make_help_button('title_uz')
            lang = ["Сиз қандай ёрдам бера оласиз?", "Сизга қандай ёрдам керак?"]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in HELP_TYPE:
            markup.add(types.KeyboardButton(i))
        # shutga next step handler bilan qilish kere agar bir busa usertype multiple tallab biladi
        if USER['user_type'] == 1:
            photo = open('photos/help_1.png', 'rb')
            bot.send_photo(chat_id, photo)
            msg = bot.send_message(chat_id=chat_id, text=lang[0], reply_markup=markup)
        else:
            photo = open('photos/help_2.png', 'rb')
            bot.send_photo(chat_id, photo)
            msg = bot.send_message(chat_id=chat_id, text=lang[1], reply_markup=markup)
        bot.register_next_step_handler(msg, get_help_types)


def get_help_types(message):
    global USERS
    global HELP_TYPE
    lang = {
        "rus": "Достаточно",
        "uzb": "Етарли",
    }
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        if USER['user_type'] == 1:
            if message.text != "Достаточно" and message.text != "Етарли":
                if 'help_type' not in USER.keys():
                    USER['help_type'] = ''
                if message.text not in HELP_TYPE:
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    for i in HELP_TYPE:
                        if str(get_id_of_help_type(HELP_TYPES, i)) not in USER['help_type'].split(',')[:-1]:
                            markup.add(types.KeyboardButton(i))
                    if 'help_type' in USER.keys():
                        markup.add(types.KeyboardButton(lang[USER["lang"]]))
                    if USER['lang'] == 'rus':
                        make_help_button('title_ru')
                        msg = bot.send_message(chat_id=chat_id, text="Пожалуйста, выберите из списка:",
                                               reply_markup=markup)
                    elif USER['lang'] == 'uzb':
                        make_help_button('title_uz')
                        msg = bot.send_message(chat_id=chat_id, text="Илтимос, руйхатдан танланг:", reply_markup=markup)
                    bot.register_next_step_handler(msg, get_help_types)
                    return
                USER['help_type'] += str(get_id_of_help_type(HELP_TYPES, message.text)) + ','
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                for i in HELP_TYPE:
                    if str(get_id_of_help_type(HELP_TYPES, i)) not in USER['help_type'].split(',')[:-1]:
                        markup.add(types.KeyboardButton(i))
                markup.add(types.KeyboardButton(lang[USER["lang"]]))
                if USER['lang'] == 'rus':
                    make_help_button('title_ru')
                    msg = bot.send_message(chat_id=chat_id, text="Еще?", reply_markup=markup)
                elif USER['lang'] == 'uzb':
                    make_help_button('title_uz')
                    msg = bot.send_message(chat_id=chat_id, text="Яна?", reply_markup=markup)
                bot.register_next_step_handler(msg, get_help_types)
            else:
                USER['help_type'] = USER['help_type'][:-1]
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
                bot.send_photo(chat_id, photo)
                msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
                bot.register_next_step_handler(msg, get_region)
        else:
            USER['help_type'] = str(get_id_of_help_type(HELP_TYPES, message.text))
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
            bot.send_photo(chat_id, photo)
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
            bot.register_next_step_handler(msg, get_region)


def get_region(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        if message.text not in REGIONS.keys():
            lang = {
                "rus": "Пожалуйста, выберите из списка:",
                "uzb": "Илтимос, руйхатдан танланг:"
            }
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for i in REGIONS.keys():
                markup.add(types.KeyboardButton(i))
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
            bot.register_next_step_handler(msg, get_region)
            return
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
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        if message.text not in REGIONS[USER['region']]:
            lang = {
                "rus": "Пожалуйста, выберите из списка:",
                "uzb": "Илтимос, руйхатдан танланг:"
            }
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for i in REGIONS[USER['region']]:
                markup.add(types.KeyboardButton(i))
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]], reply_markup=markup)
            bot.register_next_step_handler(msg, get_city)
            return
        USER['city'] = message.text

        lang = {
            "rus": "Адрес:",
            "uzb": "Манзил:"
        }
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
        bot.register_next_step_handler(msg, get_address)


def get_address(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        USER['address'] = message.text
        if USER['user_type'] == 2:
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
                "uzb": "Ўтказиб юбориш"
            }
            markup.add(types.KeyboardButton(text=lang[USER["lang"]]))
            lang = {
                "rus": "Отправить местоположение",
                "uzb": "Локацияни жўнатиш"
            }
            msg = bot.send_message(chat_id, text=lang[USER["lang"]], reply_markup=markup)
            bot.register_next_step_handler(msg, get_location)
        else:
            lang = {
                "rus": "Оставьте комментарий",
                "uzb": "Изоҳ қолдиринг",
            }
            if USER['user_type'] == 1:
                photo = open('photos/comment_1.png', 'rb')
            else:
                photo = open('photos/comment_2.png', 'rb')
            bot.send_photo(chat_id, photo)
            msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
            bot.register_next_step_handler(msg, get_comment)


def get_location(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        if message.text not in ["Пропустить", "Ўтказиб юбориш"]:
            if message.location is not None:
                USER['location'] = str(message.location.latitude) + "," + str(message.location.longitude)
            else:
                USER['location'] = message.text
        lang = {
            "rus": "Оставьте комментарий",
            "uzb": "Изоҳ қолдиринг",
        }
        if USER['user_type'] == 1:
            photo = open('photos/comment_1.png', 'rb')
        else:
            photo = open('photos/comment_2.png', 'rb')
        bot.send_photo(chat_id, photo)
        msg = bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
        bot.register_next_step_handler(msg, get_comment)


def get_comment(message):
    global USERS
    chat_id = message.chat.id
    USER = {}
    for i in USERS:
        if i['chat_id'] == chat_id:
            USER = i
    if USER['chat_id'] == chat_id:
        USER['info'] = message.text
        print(USER)
        if USER['user_type'] == 1:
            r = requests.post('https://api.birdamlik.uz/api/volunteers/create', data=USER)
        else:
            r = requests.post('https://api.birdamlik.uz/api/inneed/create', data=USER)
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
            USERS.remove(USER)

            lang = {
                "rus": "Начать сначала",
                "uzb": "Бошидан бошлаш"
            }
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton(text=lang[USER["lang"]]))

            lang = {
                "rus": "Успешно зарегистрирован",
                "uzb": "Муваффақиятли рўйхатдан ўтдингиз"
            }
            bot.send_photo(chat_id, photo)
            bot.send_message(chat_id=chat_id, text=lang[USER["lang"]])
            lang = {
                "rus": {
                    1: "Координаторы свяжутся с Вами в ближайшее время.",
                    2: "Волонтеры свяжутся с Вами в ближайшее время."
                },
                "uzb": {
                    1: "Қисқа муддат ичида координаторлар сиз билан боғланишади. Илтимос кутинг!",
                    2: "Қисқа муддат ичида сизга ёрдам берилади. Илтимос кутинг!"
                }
            }
            bot.send_message(chat_id=chat_id, text=lang[USER["lang"]][USER["user_type"]], reply_markup=markup)




if __name__ == "__main__":
    while True:
	    try:
	        bot.polling(none_stop=True, interval=0, timeout=5)
	    except Exception as e:
	        print(e)
	        time.sleep(10)
