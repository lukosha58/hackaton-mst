import database as db
from help_func2 import *

db.create_users_table()
db.create_test_result_table()
db.create_course_step_table()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # проверка на зарег, если зарег выдать меню
    def get_username(message):  # получаем ФИО
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        db.insert_user(message.from_user.id, message.from_user.username, message.text)
        bot.send_message(message.from_user.id, text="Здравствуйте", reply_markup=inline_buttons)
        delete_last_messages(message)

    if not db.get_user(message.from_user.id):
        bot.send_message(message.from_user.id, text="Пожалуйста введите ФИО")
        bot.register_next_step_handler(message, get_username)
    else:
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        bot.send_message(message.from_user.id, text="Здравствуйте", reply_markup=inline_buttons)
        bot.register_next_step_handler(message, send_menu)
    delete_last_messages(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, "Помогаю")
    delete_last_messages(message.message)


@bot.message_handler(commands=['menu'])  # menu
def send_menu(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    question = 'Меню'
    bot.send_message(message.from_user.id, text=question, reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.message_handler(commands=['text'])  # реагирует на любую надпись в чате
def wtf(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    question = 'Не понимаю что ты говоришь'
    bot.send_message(message.from_user.id, text=question, reply_markup=inline_buttons)
    delete_last_messages(message.message)


@bot.callback_query_handler(lambda message: "menu" in message.data)
def redirect_menu(message):
    send_menu(message)


@bot.callback_query_handler(lambda message: "theme" in message.data)
def view_theme(message):
    view(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message):
    callbackk(message)

@bot.callback_query_handler(lambda message: "yes" in message.data)
def test_bot(message):
    tests(message)
bot.infinity_polling()
