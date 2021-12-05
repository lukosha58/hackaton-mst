from help_func2 import *
from right_ans import check_usr_ans

token = open("token").readline()
bot = telebot.TeleBot(token)

TEST_ = {"Test_places": "theme_1"}


def testing(message):
    if message.data == "Test_places":
        file = open("test1", encoding="utf-8")
        rows = file.readlines()[::-1]
        c = len(rows)
        c2 = 1
        c3 = 2

        for i in rows:
            question, ans_1, ans_2, right_answer = i.split(";")
            answers = [[ans_1, ID_TESTS["pl"].format(c, c2)], [ans_2, ID_TESTS["pl"].format(c, c3)]]
            bot.send_message(message.message.chat.id, text=question, reply_markup=get_inline_button(answers, 2))
            c -= 1
        file.close()
    elif message.data == "Test_qr":
        print("qr")


def check_ans(message):
    if "pl" in message.data:
        check_usr_ans(message, "test1", score)
