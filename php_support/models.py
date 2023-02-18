from django.db import models


class Client(models.Model):
    username = models.CharField('Имя', max_length=50)
    is_access = models.BooleanField('Доступ', default=False)
    user_id = models.IntegerField(
        'User_id',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username


    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Devman(models.Model):
    username = models.CharField('Имя', max_length=50)
    is_access = models.BooleanField('Доступ', default=False)
    user_id = models.IntegerField(
        'User_id',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username


    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'


class Task(models.Model):
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Клиент',
        related_name='tasks',
    )
    devman = models.ForeignKey(
        'Devman',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Подрядчик',
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
        verbose_name='Статус',
        related_name='tasks',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Status(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name