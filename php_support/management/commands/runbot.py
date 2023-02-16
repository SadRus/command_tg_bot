import os
import telegram

from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from telegram.ext import Updater


load_dotenv()

tg_bot_token = os.environ['TG_BOT_TOKEN']
updater = Updater(tg_bot_token, use_context=True)


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        updater.start_polling(drop_pending_updates=True)
