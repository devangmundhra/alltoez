__author__ = 'devangmundhra'

from celery import shared_task

from apps.alltoez_profile.models import UserProfile


@shared_task
def post_save_task(pk):
    try:
        instance = UserProfile.objects.get(id=pk)
        instance.create_graph_node()
    except UserProfile.DoesNotExist:
        pass