import telebot
import database

def callb():
    if call.data == "courses":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='menu')
        keyboard.add(key_menu)
        key_t1 = telebot.types.InlineKeyboardButton(text='Какая-то тема1', callback_data='t1')
        key_t2 = telebot.types.InlineKeyboardButton(text='Какая-то тема2', callback_data='t2')
        keyboard.add(key_t1, key_t2)
        key_t3 = telebot.types.InlineKeyboardButton(text='Какая-то тема3', callback_data='t3')
        keyboard.add(key_t3)
        question = 'Выберите тему'
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == "test":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Внимание, для проходения теста вам потребует 10 минут свободного времени",
                                  show_alert=True)
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='Yes')
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='No')
        keyboard.add(key_yes, key_no)
        question = 'Вы уверены, что готовы пройти тест?'
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)

    elif call.data == "rating":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "А тут рейтинг")
    elif call.data == "menu":
        f1 = send_menu()
        f1(message = "Menu")

