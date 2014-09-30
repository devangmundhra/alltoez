#import sys
#import traceback

#from django.core.signals import got_request_exception

#def exception_printer(sender, **kwargs):
#	print >> sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))
	
#got_request_exception.connect(exception_printer)

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app