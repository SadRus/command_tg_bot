import os
import telebot

from dotenv import load_dotenv
from telebot import types
# from telebot.callback_data import CallbackData, CallbackDataFilter
from php_support import db_processing
from php_support.models import Task, Client, Status, Devman


def main():
    load_dotenv()

    token = os.getenv('TG_BOT_TOKEN')
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Исполнитель')
        item2 = types.KeyboardButton('Заказчик')
        markup.add(item1, item2)
        bot.send_message(
            message.chat.id,
            'Мы рады приветствовать вас! Кем вы являетесь?',
            reply_markup=markup,
        )


    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Исполнитель')
        item2 = types.KeyboardButton('Заказчик')
        markup.add(item1, item2)
        bot.send_message(
            message.chat.id,
            'Кем вы являетесь?',
            reply_markup=markup,
        )


    @bot.message_handler(content_types='text')
    def message_reply(message):
        username = message.from_user.username
        user_id = message.from_user.id

        # Функционал исполнителя (условное разделение)
        if message.text == 'Исполнитель':
            db_processing.create_devman(username, user_id)
            bot.send_message(
                message.chat.id,
                'Выбирай задание из списка!',
            )

        # Функционал заказчика (условное разделение)
        elif message.text == 'Заказчик':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            check_tasks = types.KeyboardButton('Мои задачи')
            create_task = types.KeyboardButton('Создать задачу')
            markup.add(check_tasks, create_task)
            db_processing.create_client(username, user_id)
            bot.send_message(
                message.chat.id,
                'Используйте меню для навигации',
                reply_markup=markup,
            )
        elif message.text == 'Создать задачу':
            bot.send_message(
                message.chat.id,
                'Используйте формат:\nЗадача - описание',
            )
        elif '-' in message.text:
            taskname, description = message.text.split('-')
            client = Client.objects.get(user_id=user_id)
            status = Status.objects.get(name='Created')
            db_processing.create_task(client, taskname, description, status)
            bot.send_message(
                message.chat.id,
                f'Задача {taskname} создана',
            )
        elif message.text == 'Мои задачи':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('Заглушка1', callback_data='Тест1')
            item2 = types.InlineKeyboardButton('Заглушка2', callback_data='Тест2')
            item3 = types.InlineKeyboardButton('Заглушка3', callback_data='Тест3')
            item4 = types.InlineKeyboardButton('Заглушка4', callback_data='Тест4')
            markup.add(item1, item2, item3, item4)
            bot.send_message(
                message.chat.id,
                'Мои задачи',
                reply_markup=markup,
            )
     
    # @bot.message_handler(regexp='\w+ - .+')
    # def create_task(message):
    #     create_task(**kwargs)
    #     bot.send_message(message.chat.id, f'Taskname: {taskname} created')

    bot.infinity_polling()


if __name__ == '__main__':
    main()
