import telebot
import copy
from telebot import types

#token = open("token").readline()
bot = telebot.TeleBot("5014702781:AAHBod4tNbiPzZuzmJxXd9JKIR8X6EybuHQ")

INLINE_MENU = [[["Курсы", "courses"], ["Тесты", "test"]], ["Рейтинг", "rating"]]
INLINE_VIEW_THEME = [[["Следующая тема", "theme_"], ["Предыдущая тема", "theme_"]], ["Меню", "menu"]]
INLINE_THEMES = [["Пароли", "theme_0"], ["Транспорт", "theme_1"], ["Qr-код", "theme_2"], ["Qr-код", "theme_3"],
                 ["Qr-код", "theme_3"], ["Qr-код", "theme_3"], ["Qr-код", "theme_3"]]
INLINE_YES_NO = [[["Да", "yes"], ["Нет", "no"]]]
BUTTON_MENU = ["Меню", ["пися", "попа"]]
COURSES = {"0": "https://telegra.ph/Password-12-04-2", "1": "https://telegra.ph/Transport-12-04-2",
           "2": "https://telegra.ph/QR-12-04"}
INLINE_TESTS = [["Вариант 1", "one"], ["Вариант 2", "two"], ["Вариант 3","three"],["Вариант 4","four"]]
Voprosi =["Вопрос 1", "Вопрос 2", "Вопрос третий"]
users_info = []


def get_keyboard_button(button_items, resize_keyboard=True, one_time_keyboard=True):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)
    for item in button_items:
        if isinstance(item, list):
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
        if isinstance(item[0], list):
            one_line_buttons = []
            for i in item:
                one_line_buttons.append(telebot.types.InlineKeyboardButton(text=i[0], callback_data=i[1]))
            inline_buttons.add(*one_line_buttons)
        else:
            inline_buttons.add(telebot.types.InlineKeyboardButton(text=item[0], callback_data=item[1]))
    return inline_buttons


def check_theme_num(data):
    for i in range(0, 4):
        if str(i) in data:
            return str(i)


def edit_inline_button(course_num, inline_view_course):
    list_courses = copy.deepcopy(inline_view_course)
    if course_num == str(0):
        del list_courses[0][1]
        list_courses[0][0][1] += str(int(course_num) + 1)
        return list_courses
    elif course_num == str(len(inline_view_course)):
        del list_courses[0][0]
        list_courses[0][0][1] += str(int(course_num) - 1)
        return list_courses
    else:
        list_courses[0][0][1] += str(int(course_num) + 1)
        list_courses[0][1][1] += str(int(course_num) - 1)

    return list_courses


def delete_last_messages(message):
    bot.delete_message(message.chat.id, message.message_id)
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass


def view(message):
    theme_num = check_theme_num(message.data)
    print(theme_num)
    print(edit_inline_button(theme_num, INLINE_VIEW_THEME))
    bot.send_message(message.message.chat.id, text=COURSES[theme_num],
                     reply_markup=get_inline_button(edit_inline_button(theme_num, INLINE_VIEW_THEME)))
    delete_last_messages(message.message)

def callbackk(message):
    if "courses" in message.data:
        course_num = check_theme_num(message.data)
        question = 'Выберите тему'
        bot.send_message(message.message.chat.id, text=question, reply_markup=get_inline_button(INLINE_THEMES))
    elif message.data == "test":
        bot.answer_callback_query(callback_query_id=message.id,
                                  text="Внимание, для проходения теста вам потребует 10 минут свободного времени",
                                  show_alert=True)

        inline_buttons = get_inline_button(INLINE_YES_NO, 2)
        question = 'Вы уверены, что готовы пройти тест?'
        bot.send_message(message.message.chat.id, text=question, reply_markup=inline_buttons)
        delete_last_messages(message.message)
    elif message.data == "yes":
        tests(message.message)
    elif message.data == "rating":
        bot.send_message(message.message.chat.id, "А тут рейтинг")
    delete_last_messages(message.message)
    bot.answer_callback_query(callback_query_id=message.id)

def tests(message):
    print("вызвалась")
    inline_buttons = get_inline_button(INLINE_TESTS, 1)
    for vopros in Voprosi:
        vopros = Voprosi[1]
    bot.send_message(message.chat.id, text=vopros, reply_markup=inline_buttons)
    if message.data == "one":
        print("+10 баллов")
        bot.send_message(message.chat.id, text="Супергуд")
    