import telebot
import database
import sqlite3
from telebot import types


bot = telebot.TeleBot("5099242576:AAEgBg9W_Wh2uDlpo32CBtQ5UbgqtlrgAz8") #2040450158:AAGUPpJtFVZ2Jf4Ewumiw6KExt_avu8hbnE
TO_CHAT_ID = 731253916

@bot.message_handler(commands=['start'])
def send_welcome(message):
    database.db_create_users_table
    # проверка на зарег, если зарег выдать меню
    bot.send_message(message.from_user.id, "Здраствуйте")
    bot.send_message(message.from_user.id, "Пожалуйста введите ФИО" )
    # передача данных в бд

@bot.message_handler(content_types=['text']) #реагирует на любую надпись в чате
def send_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2);  # наша клавиатура
    key_Courses = telebot.types.InlineKeyboardButton(text='Курсы', callback_data='courses');  # кнопка «Да»
    #keyboard.add(key_Courses);  # добавляем кнопку в клавиатуру
    key_test = telebot.types.InlineKeyboardButton(text='Тесты', callback_data='test');
    keyboard.add(key_Courses, key_test);
    #start_markup.row(key_Courses, key_test)
    key_rating = telebot.types.InlineKeyboardButton(text='Рейтинг', callback_data='rating');
    keyboard.add(key_rating);
    #start_markup.row(key_rating)
    question = 'Меню';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "courses":
        keyboard = telebot.types.InlineKeyboardMarkup();
        key_t1 = telebot.types.InlineKeyboardButton(text='Какая-то тема1', callback_data='t1');
        keyboard.add(key_t1);
        key_t2 = telebot.types.InlineKeyboardButton(text='Какая-то тема2', callback_data='t2');
        keyboard.add(key_t2);
        key_t3 = telebot.types.InlineKeyboardButton(text='Какая-то тема3', callback_data='t3');
        keyboard.add(key_t3);
        question = 'Выберите тему';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == "test":
        bot.answer_callback_query(callback_query_id=call.id, text="Внимание, для проходения теста вам потребует 10 минут свободного времени", show_alert=True)
        keyboard = telebot.types.InlineKeyboardMarkup();
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='Yes');
        keyboard.add(key_yes);
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='No');
        keyboard.add(key_no);
        question = 'Вы уверены, что готовы пройти тест?';
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)

    elif call.data == "rating":
        bot.send_message(call.message.chat.id, "А тут рейтинг");



bot.infinity_polling()