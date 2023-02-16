import os
import sqlite3
import telebot

from dotenv import load_dotenv
from telebot import types


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER)""")
        connect.commit()

        user_id = [message.chat.id]
        cursor.execute("INSERT INTO users VALUES(?);", user_id)
        connect.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Исполнитель")
        markup.add(item1)
        item2 = types.KeyboardButton("Заказчик")
        markup.add(item2)
        bot.send_message(message.chat.id, 'Мы рады приветствовать вас! Кем вы являетесь?', reply_markup=markup)


    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Исполнитель")
        markup.add(item1)
        item2 = types.KeyboardButton("Заказчик")
        markup.add(item2)
        bot.send_message(message.chat.id, 'Кем вы являетесь?', reply_markup=markup)

    @bot.message_handler(content_types='text')
    def message_reply(message):
        if message.text == "Исполнитель":
            bot.send_message(message.chat.id, "Выбирай задание из списка и вперед зарабатывать бабки!")
        elif message.text == "Заказчик":
            bot.send_message(message.chat.id, "Пиши задание, будем искать тебе помощь!")

    bot.polling()

if __name__ == '__main__':
    main()