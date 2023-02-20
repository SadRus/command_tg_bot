import logging
import os

import telebot
from dotenv import load_dotenv

import markups

load_dotenv()

API_TOKEN = os.environ.get('TG_TOKEN')

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)


def fetch_user_content(message):
    """Извлекаем данные пользователя для БД"""
    user_content = {
        'user_id': message.chat.id,
        'user_last_name': message.chat.last_name,
        'user_first_name': message.chat.first_name,
        'user_phone_number': message.contact,
        'chat_username': message.chat.username
    }
    return user_content


def check_user_category(user_id):
    """Проверяем регистрацию доступа пользователя к боту"""
    registrated_users = {
        # 'admin': [283111606, ],
        'clients': [283111606, 283111607, ],
        'contractors': [283111605, 283111608, ]
    }
    try:
        user_category = [category for category in registrated_users if user_id in registrated_users[category]][0]
    except IndexError:
        user_category = None
    return user_category


# --------------- Стартовое меню
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if check_user_category(user_id) == 'clients':
        bot.send_message(message.chat.id,
                         f"Привет, {message.chat.first_name}!",
                         reply_markup=markups.start_keyboard_for_clients())
    elif check_user_category(user_id) == 'contractors':
        bot.send_message(message.chat.id,
                         f"Привет, {message.chat.first_name}!",
                         reply_markup=markups.start_keyboard_for_contractors())
    else:
        bot.send_message(message.chat.id,
                         text='Привет!',
                         reply_markup=markups.start_keyboard_for_unregistrated_users())


@bot.message_handler(commands=['help'])
def help(message):
    reference = 'Для получения дополнительной информации:\n'
    bot.send_message(message.chat.id, reference, reply_markup=markups.help_inline_keyboard())

<<<<<<< HEAD

# --------- Вариант без удаления сообщения
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'task_help':
        bot.send_message(callback.message.chat.id,
                         text='Введите свой вопрос, отправим заказчику')
    elif callback.data == 'task_close':
        bot.send_message(callback.message.chat.id,
                         text='Статус изменен на "завершена". Требуется подтверждение клиента.')

# -------------- Вариант с удалением сообщения
@bot.callback_query_handler(func=lambda callback:True)
def check_callback(callback):
    if callback.message:
        if callback.data == 'task_help':
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.id,
                                  text='Введите свой вопрос, отправим заказчику')

        elif callback.data == 'task_close':
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.id,
                                  text='Статус изменен на "завершена". Требуется подтверждение клиента.')


bot.infinity_polling()