from django.db import models


'''
Event class
Class to store information about events
'''
class Event(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
