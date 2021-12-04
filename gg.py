import telebot
import database
import sqlite3
from telebot import types
bot = telebot.TeleBot("")
TO_CHAT_ID = 731253916
is_reg=False
database.db_create_users_table()
database.db_create_test_result_table()
database.db_create_course_step_table()

@bot.message_handler(commands= ['start'])

def start(message):
    user_id = message.chat.id
    username = message.from_user.username
    global is_reg
    if is_reg:
        msg = bot.send_message(message.from_user.id, "Вы зарегистрированы")
        bot.register_next_step_handler(msg,send_menu)
    else:
        # проверка на зарег, если зарег выдать меню
        bot.send_message(message.from_user.id, "Здраствуйте")
        bot.send_message(message.from_user.id, "Пожалуйста введите ФИО")
        database.db_insert_user(user_id, username)
        bot.send_message(message.from_user.id, "Вы прошли тест бла бла бла, вот вам меню")
        bot.send_message(message.from_user.id, "Меню")
        is_reg = True

@bot.message_handler(content_types=['text'])
def send_menu(message):
    bot.send_message(message.chat.id," ЕЕЕЕЕЕЕЕ ЬОИИИИИИИИИИИ, ты меня вызвал")
    #bot.delete_message(message.chat.id, message.message_id)
    #keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
    #key_Courses = telebot.types.InlineKeyboardButton(text='Курсы', callback_data='courses')
    #key_test = telebot.types.InlineKeyboardButton(text='Тесты', callback_data='test')
    #keyboard.add(key_Courses, key_test)
    #key_rating = telebot.types.InlineKeyboardButton(text='Рейтинг', callback_data='rating')
    #keyboard.add(key_rating)
    #question = ''
    #bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "courses":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='menu')
        keyboard.add(key_menu)
        key_t1 = telebot.types.InlineKeyboardButton(text='Какая-то тема1', callback_data='t1')
        key_t2 = telebot.types.InlineKeyboardButton(text='Какая-то тема2', callback_data='t2')
        keyboard.add(key_t1, key_t2)
        key_t3 = telebot.types.InlineKeyboardButton(text='Какая-то тема3', callback_data='t3')
        keyboard.add(key_t3)
        question = 'Выберите тему'
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == "test":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Внимание, для проходения теста вам потребует 10 минут свободного времени",
                                  show_alert=True)
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='Yes')
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='No')
        keyboard.add(key_yes, key_no)
        question = 'Вы уверены, что готовы пройти тест?'
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)

    elif call.data == "rating":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "А тут рейтинг")
    elif call.data == "menu":
        f1 = send_menu()
        f1(message = "Menu")

bot.infinity_polling()
