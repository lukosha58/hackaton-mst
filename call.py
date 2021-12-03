import telebot
import database
@bot.message_handler(content_types=['text'])  # реагирует на любую надпись в чате
def send_menu(message):
    if message.text == "Меню":
        bot.delete_message(message.chat.id, message.message_id)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)  # наша клавиатура
        key_Courses = telebot.types.InlineKeyboardButton(text='Курсы', callback_data='courses')
        key_test = telebot.types.InlineKeyboardButton(text='Тесты', callback_data='test')
        keyboard.add(key_Courses, key_test)
        key_rating = telebot.types.InlineKeyboardButton(text='Рейтинг', callback_data='rating')
        keyboard.add(key_rating)
        question = ''
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
