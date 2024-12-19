from __future__ import absolute_import, unicode_literals

from celery import shared_task

from celery.schedules import solar

import time
from celery import task 
from celery import shared_task 
# We can have either registered task 
from celery import Celery
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def add(x, y):
    return x + y

@task(name='summary') 
def send_import_summary():
    print('lol')
     # Magic happens here ... 
# or 



@shared_task 
def send_notifiction():
    print('Here I')
     # Another trick


@shared_task
def sum():
    
    print('a+b')
    return "a+b"

@shared_task
def send_hai(email):
    
    print('madhan')
    get_enrolled_user=['madhanumk@gmail.com']
    subject, from_email, to = 'Today Test', settings.EMAIL_HOST_USER, get_enrolled_user
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=get_enrolled_user)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('ki')


@shared_task
def send_mail(email):
    print("hai")
  