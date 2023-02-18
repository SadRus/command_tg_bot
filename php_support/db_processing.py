from django.utils import timezone
from php_support.models import Task, Client, Status, Devman


def create_task(client, taskname, description, status):
    Task.objects.get_or_create(
        client = client,
        devman = None,
        title = taskname,
        description = description,
        date_start = timezone.now(),
        date_end = timezone.now(),
        status = status,
    )

def create_devman(username, user_id):
    Devman.objects.get_or_create(
        username = username,
        user_id = user_id,
    )

def create_client(username, user_id):
    Client.objects.get_or_create(
        username = username,
        user_id = user_id,
    )

def get_created_tasks():
    return Task.objects.filter(status__name='Created')

def get_my_tasks(user_id):
    return Task.objects.filter(client__user_id=user_id)

# def take_task(user_id):
    # task = Devman.objects.get(user_id=user_id)
    # task.save()

# def check_for_access(username):
#     return users.objects.filter(name=username).is_access