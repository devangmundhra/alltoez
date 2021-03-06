__author__ = 'devangmundhra'

import logging

from django.core.mail import EmailMessage

from celery import shared_task

from apps.alltoez_profile.models import UserProfile

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task
def post_save_task(pk):
    try:
        instance = UserProfile.objects.get(id=pk)
        instance.create_graph_node()
    except UserProfile.DoesNotExist:
        pass


@shared_task
def send_welcome_email(email_address):
    msg = EmailMessage(from_email=("Alltoez", "noreply@alltoez.com"),
                       to=[email_address])
    msg.template_name = "Welcome To Alltoez"
    msg.send()