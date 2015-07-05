__author__ = 'devangmundhra'

import logging
from celery import shared_task

from django.core.mail import EmailMessage

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(email_address):
    msg = EmailMessage(from_email=("Alltoez", "noreply@alltoez.com"),
                       to=[email_address])
    msg.template_name = "Welcome To Alltoez"
    msg.send()