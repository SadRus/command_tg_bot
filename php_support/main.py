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

    # @bot.message_handler(regexp=r'\w+ - .+')
    # def create_task(message):
    #     bot.send_message(message.chat.id, f'Taskname: created')

    @bot.message_handler(content_types='text')
    def message_reply(message):
        username = message.from_user.username
        user_id = message.from_user.id

        # Функционал исполнителя (условное разделение)
        if message.text == 'Исполнитель':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            my_tasks = types.KeyboardButton('Мои задачи')            
            check_tasks = types.KeyboardButton('Актуальные задачи')
            markup.add(my_tasks, check_tasks)
            db_processing.create_devman(username, user_id)
            bot.send_message(
                message.chat.id,
                'Выбирай задание из списка!',
                reply_markup=markup,
            )
        elif message.text == 'Актуальные задачи':
            markup = types.InlineKeyboardMarkup()
            for task in db_processing.get_created_task():
                item = types.InlineKeyboardButton(task.title , callback_data='Тест1')
                markup.add(item)
            bot.send_message(
                message.chat.id,
                'Актуальные задачи',
                reply_markup=markup,
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
     

    bot.infinity_polling()


if __name__ == '__main__':
    main()
