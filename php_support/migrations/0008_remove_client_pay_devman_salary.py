# Generated by Django 4.1.7 on 2023-02-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('php_support', '0007_client_pay_task_note_task_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='pay',
        ),
        migrations.AddField(
            model_name='devman',
            name='salary',
            field=models.IntegerField(default=1000, verbose_name='Ставка'),
        ),
    ]