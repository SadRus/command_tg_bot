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



def get_created_tasks(user_id):
    return Task.objects.filter(status__name='Created')

# devman funcs
def take_task(user_id):
    Devman.objects.get(user_id=user_id)

def get_devman_all_tasks(user_id):
    return Task.objects.filter(devman__user_id=user_id)
    
def get_devman_inprogress_tasks(user_id):
    return Task.objects.filter(devman__user_id=user_id, status__name='In progress')

def get_devman_done_tasks(user_id):
    return Task.objects.filter(devman__user_id=user_id, status__name='Done')

def check_devman_access(user_id):
    if Devman.objects.get(user_id).is_access:
        return True
    return False


# client funcs
def get_client_all_tasks(user_id):
    return Task.objects.filter(client__user_id=user_id)

def get_client_inprogress_tasks(user_id):
    return Task.objects.filter(client__user_id=user_id, status__name='In progress')

def get_client_done_tasks(user_id):
    return Task.objects.filter(client__user_id=user_id, status__name='Done')

def check_client_access(user_id):
    if Client.objects.get(user_id).is_access:
        return True
    return False