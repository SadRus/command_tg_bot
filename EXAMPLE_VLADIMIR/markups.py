import telebot
from telebot import types



def start_keyboard_for_unregistrated_users():
    """Стартовое меню для незарегистрированных пользователей"""
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_start = types.KeyboardButton(text='регистрация')
    btn_help = types.KeyboardButton(text='узнать больше')
    return start_keyboard.add(btn_start, btn_help)


def start_keyboard_for_clients():
    """Стартовое меню для Заказчика"""
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_task = types.KeyboardButton(text='задание')
    btn_update_task = types.KeyboardButton(text='обновить задание')
    btn_all_tasks = types.KeyboardButton(text='мои задания')
    btn_help = types.KeyboardButton(text='сообщить о проблеме')
    btn_subscription = types.KeyboardButton(text='продлить подписку')
    return start_keyboard.add(btn_task, btn_all_tasks, btn_update_task, btn_help, btn_subscription)


def start_keyboard_for_contractors():
    """Стартовое меню для Исполнителя"""
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_task = types.KeyboardButton(text='взять задание')
    btn_all_tasks = types.KeyboardButton(text='мои задания')
    btn_help = types.KeyboardButton(text='сообщить о проблеме')
    return start_keyboard.add(btn_task, btn_all_tasks, btn_help)


def help_inline_keyboard():
    """Заглушка для запроса помощи в стартовом меню для всех"""
    help_inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_description = types.InlineKeyboardButton(text='узнать условия', url='https://dvmn.org/modules/')
    btn_contact_us  = types.InlineKeyboardButton(text='сообщить о проблеме', url='https://dvmn.org/contacts/')
    return help_inline_keyboard.add(btn_description, btn_contact_us)


def help_inline_keyboard_for_contractor():
    """
    Сценарий: кнопка для отправки вопроса Заказчику,
    прикрепляется к каждому заданию Исполнителя, имеющему статус 'в работе'
    """
    task_help_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_task_help = types.InlineKeyboardButton(text='нужна информация', callback_data='task_help')
    btn_task_close = types.InlineKeyboardButton(text='завершить', callback_data='task_close')
    return task_help_keyboard.add(btn_task_help, btn_task_close)

