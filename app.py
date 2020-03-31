from flask import Flask, request
from views import demo
import os
import telebot
from telebot import types
###############################USER_INFO#######################
USER={}


###############################################################
##########################Bot_setup###############################
API_TOKEN = '868081058:AAFSj3Q2diNtIJnd0pt1xtC02HhhP06qxRs'
bot = telebot.TeleBot(API_TOKEN)
###################################################################
app = Flask(__name__)

app.add_url_rule('/demo',  methods=['POST', 'GET'], view_func=demo)

LANGUAGE_BUTTON_RUSSIAN = "🇷🇺--Руский--🇷🇺"
LANGUAGE_BUTTON_UZBEK = "🇺🇿--УЗБЕКЧА--🇺🇿"
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_RUSSIAN))
    markup.add(types.KeyboardButton(LANGUAGE_BUTTON_UZBEK))
    bot.send_message(chat_id=chat_id, text="Tilni tanlang \n выберите язык ", reply_markup=markup)

def uzb_lang_button_checker(message):
    return message.text == LANGUAGE_BUTTON_UZBEK

def ru_lang_button_checker(message):
    return message.text ==LANGUAGE_BUTTON_RUSSIAN

@bot.message_handler(func=uzb_lang_button_checker)
def start_login_uzb(message):
    global USER
    chat_id = message.chat.id
    USER['chat_id']=chat_id
    USER['lang']='uzb'
    msg = bot.send_message(chat_id=chat_id, text="uzbek tilini tanladingiz")
    # bot.register_next_step_handler(msg, get_and_forward_feedback)

@bot.message_handler(func=ru_lang_button_checker)
def start_login_ru(message):
    global USER
    chat_id = message.chat.id
    USER['chat_id']=chat_id
    USER['lang']='uzb'
    msg = bot.send_message(chat_id=chat_id, text="вы выбрали русский язык")
    # bot.register_next_step_handler(msg, get_and_forward_feedback)


@app.route('/' + API_TOKEN , methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://75039edb.ngrok.io/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 5000)))