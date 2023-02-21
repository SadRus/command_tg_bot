import os
import telebot

from django.utils import timezone
from dotenv import load_dotenv
from telebot import types
from php_support import db, markups
from php_support.models import Task, Client, Status, Devman


def main():
    load_dotenv()

    token = os.getenv('TG_BOT_TOKEN')
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            'Мы рады приветствовать вас! Кем вы являетесь?',
            reply_markup=markups.start_keyboard_for_all_users(),
        )

    @bot.message_handler(content_types='text')
    def message_reply(message):
        username = message.from_user.username
        user_id = message.from_user.id

        # Функционал исполнителя (условное разделение)
        if message.text == 'Подрядчик':
            db.create_devman(username, user_id)
            if Devman.objects.get(user_id=user_id).is_access:
                bot.send_message(
                    message.chat.id,
                    'Используйте меню для навигации',
                    reply_markup=markups.start_keyboard_for_devman(),
                )
            else:
                bot.send_message(
                    message.chat.id,
                    'Отказано в доступе. Обратитесь к администратору.',
                )
        elif message.text == 'Актуальные задачи':
            for task in db.get_created_tasks(user_id):
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(
                    'взять в работу',
                    callback_data=f'take_task{task.id}'
                )
                item2 = types.InlineKeyboardButton(
                    'посмотреть',
                    callback_data='btn2'
                )
                markup.add(item1, item2)
                bot.send_message(
                    message.chat.id,
                    text = f'{task.title} - {task.description}',
                    reply_markup=markup,
                )
        elif message.text == 'Принятые в работу':
            for task in db.get_devman_inprogress_tasks(user_id):
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(
                    'задать вопрос',
                    callback_data='btn1'
                )
                item2 = types.InlineKeyboardButton(
                    'завершить',
                    callback_data=f'end_task{task.id}'
                )
                markup.add(item1, item2)
                bot.send_message(
                    message.chat.id,
                    text = f'Заголовок: {task.title}\n'
                           f'Описание: {task.description}',
                    reply_markup=markup,
                )
        elif message.text == 'Завершенные задачи':
            for task in db.get_devman_done_tasks(user_id):
                bot.send_message(
                    message.chat.id,
                    text = f'Заголовок: {task.title}\n'
                           f'Описание: {task.description}',
                )
        elif message.text == 'Статистика':
            total_task_done = Task.objects \
                                  .filter(devman__user_id=user_id,
                                          status__name='Done') \
                                  .count()
            salary = Devman.objects.get(user_id=user_id).salary
            total_money = total_task_done * salary
            bot.send_message(
                message.chat.id,
                text = f'Всего задач закрыто: {total_task_done}\n'
                       f'Ставка: {salary}\n'
                       f'Всего заработано: {total_money} rub'
            )

        # Функционал заказчика (условное разделение)
        elif message.text == 'Заказчик':
            db.create_client(username, user_id)
            if Client.objects.get(user_id=user_id).is_access:
                bot.send_message(
                    message.chat.id,
                    'Используйте меню для навигации',
                    reply_markup=markups.start_keyboard_for_client(),
                )
            else:
                bot.send_message(
                    message.chat.id,
                    'Отказано в доступе. Обратитесь к администратору.',
                )
        elif message.text == 'Создать задачу':
            bot.send_message(
                message.chat.id,
                ('Используйте формат:\nЗадача - описание\n'
                 '(в описании укажите данные для доступа '
                 'к PHP-админке сайта)'),
            )
        elif '-' in message.text:
            taskname, description = message.text.split('-')
            client = Client.objects.get(user_id=user_id)
            status = Status.objects.get(name='Created')
            db.create_task(client, taskname,
                                      description, status)
            bot.send_message(
                message.chat.id,
                f'Задача {taskname} создана',
            )
        elif message.text == 'Размещенные задачи':
            for task in db.get_created_tasks(user_id):
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(
                    'дополнить',
                    callback_data='btn1'
                    )
                item2 = types.InlineKeyboardButton(
                    'отменить', 
                    callback_data='btn2')
                markup.add(item1, item2)
                bot.send_message(
                    message.chat.id,
                    text = f'Заголовок: {task.title}\n'
                           f'Описание: {task.description}',
                    reply_markup=markup,
                )
        elif message.text == 'В работе':
            for task in db.get_client_inprogress_tasks(user_id):
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(
                    'дополнить', 
                    callback_data='btn1')
                markup.add(item1)
                bot.send_message(
                    message.chat.id,
                    text = f'Заголовок: {task.title}\n'
                           f'Описание: {task.description}',
                    reply_markup=markup,
                )
        elif message.text == 'Завершено':
            for task in db.get_client_done_tasks(user_id):
                markup = types.InlineKeyboardMarkup()
                item1 = types.InlineKeyboardButton(
                    'добавить отзыв', 
                    callback_data='btn1')
                markup.add(item1)
                bot.send_message(
                    message.chat.id,
                    text = f'Заголовок: {task.title}\n'
                           f'Описание: {task.description}',
                    reply_markup=markup,
                )

    # Обработчик inlinekeyboard (условное разделение)
    @bot.callback_query_handler(func=lambda f: True)
    def callback_button1(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        if Devman.objects.get(user_id=user_id).is_access:
            if 'take_task' in callback_query.data:
                task_id = int(callback_query.data[9:])
                task = Task.objects.get(id=task_id)
                task.devman = Devman.objects.get(
                    user_id=callback_query.from_user.id
                )
                task.status = Status.objects.get(name='In progress')
                task.save()
                bot.answer_callback_query(
                    callback_query.id,
                    'Задача взята в работу',
                )
            elif 'end_task' in callback_query.data:
                task_id = int(callback_query.data[8:])
                task = Task.objects.get(id=task_id)
                task.status = Status.objects.get(name='Done')
                task.date_end = timezone.now()
                task.save()
                bot.answer_callback_query(
                    callback_query.id,
                    'Задача сдана заказчику',
                )       
        else:
            bot.answer_callback_query(
                callback_query.id,
                show_alert=True,
                text='У вас нет доступа, оплатите подписку',
            )

    bot.infinity_polling()


if __name__ == '__main__':
    main()
