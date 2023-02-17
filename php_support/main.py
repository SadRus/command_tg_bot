import os
import telebot

from dotenv import load_dotenv
from django.utils import timezone
from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from php_support.models import Task, Client, Status, Devman


# def check_for_access(username):
#     return users.objects.filter(name=username).is_access


def main():
    load_dotenv()

    token = '5973930091:AAFjdWwIWWy-8BYXGBxrEjhHk_VVuMh2uVc'
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
    def create_task(message):
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
        if message.text == "Исполнитель":
            devman = Devman(
                name = message.from_user.username,
                user_id = message.from_user.id,
            )
            devman.save()
            bot.send_message(message.chat.id, "Выбирай задание из списка и вперед зарабатывать бабки!")
        elif message.text == "Заказчик":
            client = Client(
                name = message.from_user.username,
                user_id = message.from_user.id,
            )
            client.save()
            bot.send_message(message.chat.id, "Пиши задание, будем искать тебе помощь!")
        elif '-' in message.text:
            taskname, description = message.text.split('-')
            task = Task(
                client = None,
                devman = None,
                title = taskname,
                description = description,
                date_start = timezone.now(),
                date_end = timezone.now(),
                status = None,
            )
            task.save()

            bot.send_message(message.chat.id, f'Taskname: {taskname} created')


    bot.infinity_polling()


if __name__ == '__main__':
    main()
