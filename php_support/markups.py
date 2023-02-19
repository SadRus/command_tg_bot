from telebot import types


def start_keyboard_for_all_users():
    """Стартовое меню для всех пользователей"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Заказчик')
    btn2 = types.KeyboardButton(text='Подрядчик')
    return keyboard.add(btn1, btn2)


def start_keyboard_for_client():
    """Стартовое меню для заказчиков"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Создать задачу')
    btn2 = types.KeyboardButton(text='Размещенные задачи')
    btn3 = types.KeyboardButton(text='В работе')
    btn4 = types.KeyboardButton(text='Завершено')
    return keyboard.add(btn1, btn2, btn3, btn4)


def start_keyboard_for_devman():
    """Меню для подрядчиков"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Актуальные задачи')
    btn2 = types.KeyboardButton(text='Принятые в работу')
    btn3 = types.KeyboardButton(text='Завершенные задачи')
    btn4 = types.KeyboardButton(text='Статистика')
    return keyboard.add(btn1, btn2, btn3, btn4)


