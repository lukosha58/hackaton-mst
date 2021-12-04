import telebot
import copy
from telebot import types

token = open("token").readline()
bot = telebot.TeleBot(token)

INLINE_MENU = [[["Курс", "courses"], ["Тесты", "test"]], ["Рейтинг", "rating"]]
INLINE_VIEW_THEME = [[["Следующая тема", "theme_"], ["Предыдущая тема", "theme_"]], ["Завершить курс", "final_courses"],
                     ["Меню", "menu"]]
INLINE_THEMES = [["Пароли", "theme_0"], ["Транспорт", "theme_1"], ["Qr-код", "theme_2"], ["4", "theme_3"],
                 ["5", "theme_4"], ["6", "theme_5"], ["7", "theme_6"], ["8", "theme_7"], ["Меню", "menu"]]
INLINE_YES_NO = [[["Да", "yes"], ["Нет", "no"]]]
BUTTON_MENU = ["Меню"]
COURSES = {"0": "https://telegra.ph/Password-12-04-2", "1": "https://telegra.ph/Transport-12-04-2",
           "2": "https://telegra.ph/QR-12-04", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7"}
texts_tree = {"hello": "Здравствуйте, {}",
              "reg_fio": "Введите своё ФИО",
              "help": "Помогаю",
              "wtf": "Не понимаю что ты пишешь",
              "menu": "Меню",
              "done_course": "Вау ты прошёл весь курс",
              "not_done_course": "Нет, ещё не все курсы сделаны",
              "choose_themes": "Выберите тему",
              "are_you_ready": "Вы уверены, что готовы пройти тест?",
              "rating": "А тут рейтинг"}


def is_done_full_course(db, message):
    info = db.get_course_step(message.from_user.id)
    for i in range(1, len(info)):
        if info[i] in (False, None):
            return False
    return True


def get_bool_theme(inline_items, db, message):
    inline_items = copy.deepcopy(inline_items)
    users_done_theme = db.get_course_step(message.from_user.id)
    for i in range(len(inline_items) - 1):
        if users_done_theme[i + 1]:
            inline_items[i][0] += " ✅"
        else:
            inline_items[i][0] += " ❌"
    return inline_items


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
    for i in range(len(INLINE_THEMES) - 1):
        if str(i) in data:
            return str(i)


def edit_inline_button(theme_num, inline_view_course, db, message):
    list_courses = copy.deepcopy(inline_view_course)

    if theme_num == str(0):
        del list_courses[0][1]
        list_courses[0][0][1] += str(int(theme_num) + 1)
        return list_courses
    elif theme_num == str(len(INLINE_THEMES) - 2):
        list_courses[0][1][1] += str(int(theme_num) - 1)
        return list_courses
    else:
        list_courses[0][0][1] += str(int(theme_num) + 1)
        list_courses[0][1][1] += str(int(theme_num) - 1)
    if not is_done_full_course(db, message):
        del list_courses[1]
    return list_courses


def delete_last_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
