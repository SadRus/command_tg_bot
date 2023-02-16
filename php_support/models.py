from django.db import models


class Client(models.Model):
    name = models.CharField('Имя', max_length=50)
    is_access = models.BooleanField('Доступ')
    chat_id = models.IntegerField('chat_id')


class Devman(models.Model):
    name = models.CharField('Имя', max_length=50)
    is_access = models.BooleanField('Доступ')
    chat_id = models.IntegerField('chat_id')


class Task(models.Model):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name='Задача',
        related_name='tasks',
    )
    devman = models.ForeignKey(
        'Devman',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Задача',
        related_name='tasks',
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    date_start = models.DateTimeField('Дата и время начала')
    date_end = models.DateTimeField('Дата и время конца')
    status = models.ForeignKey(
        'Status',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Задача',
        related_name='tasks',
    )


class Status(models.Model):
    name = models.CharField('Название', max_length=200)
