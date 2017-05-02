import datetime

import pushpad
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import DB_Due, DB_Tasks, DB_User

try:
    token_file = open('pushpad_token.txt', 'r')
    push_token = token_file.read()
    push_project = pushpad.Pushpad(auth_token=push_token, project_id=3480)
except IOError:
    print("pushpad_token.txt does not exist, please make one.")


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'notifications.MyCronJob'

    def do(self):
        check_to_notify()


def fire_safari(task):
    pass


def fire_email(task):
    user = User.objects.get(id=task.user)
    email = user.email
    send_mail(
        'Canvas++ Notification',
        'REMINDER: ' + task.task_name + ' is due by ' + task.end_date,
        'canvasplusplus@gmail.com',
        [email],
        fail_silently=False,
    )
    pass


def fire_chrome(task):
    pass


def notify_all(task):
    print(task)
    fire_safari(task)
    fire_email(task)
    fire_chrome(task)


def check_to_notify():
    list_of_due = DB_Due.objects.all()
    for task in list_of_due:
        if task.due < datetime.datetime.now():
            real_task = DB_Tasks.objects.get(id=task.id)
            notify_all(real_task)
            task.delete()
