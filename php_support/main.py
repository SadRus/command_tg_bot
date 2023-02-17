import os
import telebot

from dotenv import load_dotenv
from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from php_support import db_processing
from php_support.models import Task, Client, Status, Devman


# def check_for_access(username):
#     return users.objects.filter(name=username).is_access


def main():
    load_dotenv()

    token = os.getenv('TG_BOT_TOKEN')
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Исполнитель")
        markup.add(item1)
        item2 = types.KeyboardButton("Заказчик")
        markup.add(item2)
        bot.send_message(message.chat.id, 'Мы рады приветствовать вас! Кем вы являетесь?', reply_markup=markup)


    @bot.message_handler(commands=['create_task'])
    def create_task_command(message):
        bot.send_message(message.chat.id, 'Great! Create the task. Use format:\ntaskname - description')


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
        username = message.from_user.username
        user_id = message.from_user.id

        if message.text == "Исполнитель":
            db_processing.create_devman(username, user_id)
            bot.send_message(message.chat.id, "Выбирай задание из списка!")

        elif message.text == "Заказчик":
            db_processing.create_client(username, user_id)
            bot.send_message(message.chat.id, "Пиши задание, будем искать тебе помощь!")

        elif '-' in message.text:
            taskname, description = message.text.split('-')
            client = Client.objects.get(user_id=user_id)
            status = Status.objects.get(name='Created')

            db_processing.create_task(client, taskname, description, status)
            bot.send_message(message.chat.id, f'Task: {taskname} created')
    
    # @bot.message_handler(regexp='\w+ - .+')
    # def create_task(message):
    #     create_task(**kwargs)
    #     bot.send_message(message.chat.id, f'Taskname: {taskname} created')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
