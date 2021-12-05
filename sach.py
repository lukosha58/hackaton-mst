import database as db
from help_func2 import *
import emoji

db.create_users_table()
db.create_test_result_table()
db.create_course_step_table()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # проверка на зарег, если зарег выдать меню
    def get_username(message):  # получаем ФИО
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        db.insert_user(message.from_user.id, message.from_user.username, message.text)
        bot.send_message(message.from_user.id, text=texts_tree['hello'].format(message.text),
                         reply_markup=inline_buttons)
        delete_last_messages(message)

    if not db.get_user(message.from_user.id):
        bot.send_message(message.from_user.id, text=texts_tree['reg_fio'])
        bot.register_next_step_handler(message, get_username)
    else:
        inline_buttons = get_inline_button(INLINE_MENU, 2)
        bot.send_message(message.from_user.id, text=texts_tree['hello'].format(message.from_user.username),
                         reply_markup=inline_buttons)
        bot.register_next_step_handler(message, send_menu)
    delete_last_messages(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, texts_tree['help'])
    delete_last_messages(message.message)


@bot.message_handler(commands=['menu'])  # реагирует на любую надпись в чате
def send_menu(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['menu'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.message_handler(content_types=['text'])  # реагирует на любую надпись в чате
def wtf(message):
    inline_buttons = get_inline_button(INLINE_MENU, 2)
    bot.send_message(message.from_user.id, text=texts_tree['wtf'], reply_markup=inline_buttons)
    delete_last_messages(message)


@bot.callback_query_handler(lambda message: "menu" in message.data)
def redirect_menu(message):
    delete_last_messages(message.message)
    send_menu(message)


@bot.callback_query_handler(lambda message: "theme" in message.data)
def view_theme(message):
    theme_num = check_theme_num(message.data)
    db.update_course_step(theme_num, message.from_user.id, True)
    bot.send_message(message.from_user.id, text=COURSES[theme_num],
                     reply_markup=get_inline_button(edit_inline_button(theme_num, INLINE_VIEW_THEME, db, message)))
    delete_last_messages(message.message)

@bot.callback_query_handler(lambda message: "Test" in message.data)
def test(message):
    if message.data == "Test_places":
        file = open("test1", encoding="utf-8")
        for i in file.readlines():
            question, ans_1, ans_2 = i.split(";")
            answers = [[ans_1, "ans_1"], [ans_2, "ans_2"]]
            bot.send_message(message.message.chat.id, text=question, reply_markup=get_inline_button(answers, 2))
    elif message.data == "Test_qr":
        print("qr")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(message):
    callbackk(message)


bot.infinity_polling()