import telebot
import copy
from telebot import types

token = open("token").readline()
bot = telebot.TeleBot(token)

INLINE_MENU = [[["Курсы", "courses"], ["Тесты", "test"]], ["Рейтинг", "rating"]]
INLINE_VIEW_THEME = [[["Следующая тема", "theme_"], ["Предыдущая тема", "theme_"]], ["Меню", "menu"]]
INLINE_THEMES = [["Пароли", "theme_0"], ["Транспорт", "theme_1"], ["Qr-код", "theme_2"], ["Qr-код", "theme_3"],
                 ["Qr-код", "theme_3"], ["Qr-код", "theme_3"], ["Qr-код", "theme_3"]]
INLINE_YES_NO = [[["Да", "yes"], ["Нет", "no"]]]
BUTTON_MENU = ["Меню", ["пися", "попа"]]
COURSES = {"0": "https://telegra.ph/Password-12-04-2", "1": "https://telegra.ph/Transport-12-04-2",
           "2": "https://telegra.ph/QR-12-04"}
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
