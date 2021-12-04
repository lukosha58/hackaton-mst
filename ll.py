import telebot
import database

token = open("token").readline()
bot = telebot.TeleBot(token)
INLINE_MENU = [(("Курсы", "courses"), ("Тесты", "test")), ("Рейтинг", "rating")]
INLINE_THEMES = [("Тема 1", "theme_1"), ("Тема 2", "theme_2")]
INLINE_YES_NO = [(("Да", "yes"), ("Нет", "no"))]
BUTTON_MENU = ["Меню", ("пися", "попа")]


def delete_last_messages(message):
    bot.delete_message(message.chat.id, message.message_id)
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass


def get_inline_button(inline_items, row_width=3):
    inline_buttons = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    for item in inline_items:
        if isinstance(item[0], tuple):
            one_line_buttons = []
            for i in item:
                one_line_buttons.append(telebot.types.InlineKeyboardButton(text=i[0], callback_data=i[1]))
            inline_buttons.add(*one_line_buttons)
        else:
            inline_buttons.add(telebot.types.InlineKeyboardButton(text=item[0], callback_data=item[1]))
    return inline_buttons


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "courses":
        inline_buttons = get_inline_button(INLINE_THEMES)
        question = 'Выберите тему'
        bot.send_message(call.message.chat.id, text=question, reply_markup=inline_buttons)
    elif call.data == "test":
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Внимание, для проходения теста вам потребует 10 минут свободного времени",
                                  show_alert=True)

        inline_buttons = get_inline_button(INLINE_YES_NO, 2)
        question = 'Вы уверены, что готовы пройти тест?'
        bot.send_message(call.message.chat.id, text=question, reply_markup=inline_buttons)

    elif call.data == "rating":
        bot.send_message(call.message.chat.id, "А тут рейтинг")
    delete_last_messages(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
