from help_func2 import *

token = open("token").readline()
bot = telebot.TeleBot(token)


def testing(message):
    if message.data == "Test_places":
        file = open("test1", encoding="utf-8")

        for i in file.readlines():
            question, ans_1, ans_2 = i.split(";")
            answers = [[ans_1, f"ans_1"], [ans_2, "ans_2"]]
            bot.send_message(message.message.chat.id, text=question, reply_markup=get_inline_button(answers, 2))
    elif message.data == "Test_qr":
        print("qr")
