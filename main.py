import telebot
import database as db
import sqlite3
from telebot import types

token = open("token").readline()
bot = telebot.TeleBot(token)

db.create_users_table()
db.create_test_result_table()
db.create_course_step_table()

INLINE_MENU = [(("Курсы", "courses"), ("Тесты", "test")), ("Рейтинг", "rating")]
INLINE_THEMES = [("Тема 1", "theme_1"), ("Тема 2", "theme_2")]
INLINE_YES_NO = [(("Да", "yes"), ("Нет", "no"))]
BUTTON_MENU = ["Меню", ("пися", "попа")]


def get_keyboard_button(button_items, resize_keyboard=True, one_time_keyboard=True):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)
    for item in button_items:
        if isinstance(item, tuple):
            one_line_buttons = []
            for i in item:
                one_line_buttons.append(telebot.types.KeyboardButton(i))
            keyboard.add(*one_line_buttons)
        else:
            keyboard.add(telebot.types.KeyboardButton(text=item))
    return keyboard


def get_inline_button(inline_items, row_width=3):
    inline_buttons = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    for item in inline_items:
        if isinstance(item[0], tuple):
            one_line_buttons = []
            for i in item:
                one_line_buttons.append(telebot.types.InlineKeyboardButton(text=i[0], callback_data=i[1]))
            inline_buttons.add(*one_line_buttons)
        else:
            inline_buttons.add(telebot.types.InlineKeyboardButton(text=item[0], callback_data=item[1]))
    return inline_buttons


def delete_last_messages(message):
    bot.delete_message(message.chat.id, message.message_id)
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except :
        pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # проверка на зарег, если зарег выдать меню
    def get_username():  # получаем ФИО
        db.insert_user(message.from_user.id, message.from_user.username, message.text)
        bot.send_message(message.from_user.id, "Здраствуйте")

    if not db.get_user(message.from_user.id):
        bot.send_message(message.from_user.id, "Пожалуйста введите ФИО")
        bot.register_next_step_handler(message, get_username)
    else:
        bot.send_message(message.from_user.id, "Здраствуйте")
        bot.register_next_step_handler(message, send_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, "Помогаю")
    delete_last_messages(message)


@bot.message_handler(content_types=['text'])  # реагирует на любую надпись в чате
def send_menu(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    question = 'Меню'
    bot.send_message(message.from_user.id, text=question, reply_markup=inline_buttons)

    delete_last_messages(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "courses":
        inline_buttons = get_inline_button(INLINE_THEMES)
        question = 'Выберите тему'
        bot.send_message(call.message.chat.id, text=question, reply_markup=inline_buttons)
    elif call.data == "test":
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Внимание, для проходения теста вам потребует 10 минут свободного времени",
                                  show_alert=True)

        inline_buttons = get_inline_button(INLINE_YES_NO, 2)
        question = 'Вы уверены, что готовы пройти тест?'
        bot.send_message(call.message.chat.id, text=question, reply_markup=inline_buttons)

    elif call.data == "rating":
        bot.send_message(call.message.chat.id, "А тут рейтинг")
    delete_last_messages(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


bot.infinity_polling()
