import telebot
import copy
import database as db
from telebot import types

token = open("token").readline()
bot = telebot.TeleBot(token)

INLINE_MENU = [[["Курс", "courses"], ["Тесты", "TEST"]], ["Рейтинг", "rating"]]
INLINE_VIEW_THEME = [[["Следующая тема", "theme_"], ["Предыдущая тема", "theme_"]], ["Завершить курс", "final_courses"],
                     ["Меню", "menu"]]
INLINE_THEMES = [["Пароли", "theme_0"], ["Общественные сети", "theme_1"], ["Qr-код", "theme_2"],
                 ["Личные данные", "theme_3"],
                 ["Социальная инженерия", "theme_4"], ["Физическая безопасность", "theme_5"], ["Фишинг", "theme_6"],
                 ["Меню", "menu"]]
INLINE_TEST_NUMBERS = [["Тест по теме: Общественные сети", "Test_places"], ["Тест по теме: Фишинг", "Test_phishing"],
                       ["Тест по теме: Социальная инженерия", "Test_social"],
                       ["Тест по теме: Личные данные \n в интернете", "Test_osint"],
                       ["Тест по теме: Пароли", "Test_passwords"],
                       ["Тест по теме: Физическая безопасность", "Test_physical"],
                       ["Тест по теме: QR коды", "Test_qr"]]
INLINE_YES_NO = [[["Да", "yes"], ["Нет", "no"]]]
BUTTON_MENU = ["Меню"]
ID_TESTS = {"pl": "pl_{}_{}"}
COURSES = {"0": "https://telegra.ph/Password-12-04-2", "1": "https://telegra.ph/Transport-12-04-2",
           "2": "https://telegra.ph/QR-12-04", "3": "https://telegra.ph/Lichnye-dannye-12-05",
           "4": "https://telegra.ph/Socialnaya-inzheneriya-12-05",
           "5": "https://telegra.ph/Fizicheskaya-bezopasnost-12-04",
           "6": "https://telegra.ph/Fishing-12-04"}
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

score = 0


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


def is_done_full_course(db, message):
    info = db.get_course_step(message.from_user.id)
    for i in range(1, len(info)):
        if info[i] in (False, None):
            return False
    return True


def edit_inline_button(theme_num, inline_view_course, db, message):
    list_courses = copy.deepcopy(inline_view_course)

    if theme_num == str(0):
        del list_courses[0][1]
        list_courses[0][0][1] += str(int(theme_num) + 1)
    elif theme_num == str(len(INLINE_THEMES) - 2):
        del list_courses[0][0]
        list_courses[0][0][1] += str(int(theme_num) - 1)
    else:
        list_courses[0][0][1] += str(int(theme_num) + 1)
        list_courses[0][1][1] += str(int(theme_num) - 1)
    if not is_done_full_course(db, message):
        del list_courses[1]
    return list_courses


def delete_last_messages(message, all_back=True):
    if all_back:
        for i in range(10):
            try:
                bot.delete_message(message.chat.id, message.message_id - i)
            except:
                pass

    else:
        bot.delete_message(message.chat.id, message.message_id)


def callbackk(message):
    if "courses" in message.data:
        if "final" in message.data:
            if is_done_full_course(db, message):
                bot.send_message(message.from_user.id, text=texts_tree['done_course'],
                                 reply_markup=get_inline_button(INLINE_MENU))
            else:
                bot.send_message(message.from_user.id, text=texts_tree['not_done_course'],
                                 reply_markup=get_inline_button(get_bool_theme(INLINE_THEMES, db, message)))
        else:
            if not db.get_course_step(message.from_user.id):
                db.insert_course_step(0, message.from_user.id, False)
            bot.send_message(message.from_user.id, text=texts_tree['choose_themes'],
                             reply_markup=get_inline_button(get_bool_theme(INLINE_THEMES, db, message)))
    elif "TEST" in message.data:
        if not db.get_result(message.from_user.id):
            db.insert_test_result(message.from_user.id)
        bot.send_message(message.from_user.id, text=texts_tree["choose_themes"],
                         reply_markup=get_inline_button(INLINE_TEST_NUMBERS, 2))

    elif message.data == "rating":
        bot.send_message(message.from_user.id, text=texts_tree["rating"])

    delete_last_messages(message.message)
    bot.answer_callback_query(callback_query_id=message.id)


def testing(message):
    pass
