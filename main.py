import telebot  # библиотека для работы с ботом
from telebot import types  # модуль для работы с кнопками

token = open("token").readline()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start']) #приветсвие при команде /start
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка") #добавление одной кнопки
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Кнопка": #ответ на нажатие кнопки
        pass


bot.infinity_polling()
