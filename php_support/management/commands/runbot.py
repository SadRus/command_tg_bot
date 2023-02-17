from django.core.management.base import BaseCommand
from php_support.main import main


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Uses to run a bot'

    def handle(self, *args, **kwargs):
        main()
