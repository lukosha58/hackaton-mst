from help_func2 import *

token = open("token").readline()
bot = telebot.TeleBot(token)


def testing(message):
    c = 1
    c2 = 1
    c3 = 2
    if message.data == "Test_places":
        file = open("test1", encoding="utf-8")

        for i in file.readlines()[::-1]:
            question, ans_1, ans_2, right_answer = i.split(";")
            answers = [[ans_1, ID_TESTS["pl"].format(c, c2)], [ans_2, ID_TESTS["pl"].format(c, c3)]]
            bot.send_message(message.message.chat.id, text=question, reply_markup=get_inline_button(answers, 2))
            print(answers)

            c += 1
        file.close()
    elif message.data == "Test_qr":
        print("qr")
    elif "pl" in message.data:
        print(message.data)


def check_ans(message):
    if "pl" in message.data:
        print(message.data)
