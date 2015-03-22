from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.template import Context

import threading, sys, traceback

try:
	import mandrill
except:
	pass

# ------------------------------
# MANDRILL METHODS (http://mandrillapp.com)
# ------------------------------
def get_mandrill_client():
	"""
	Gets the mandrill client if it exists for this project
	"""
	try:
		MANDRILL_API_KEY = settings.MANDRILL_API_KEY
		MANDRILL_TRACKING_DOMAIN = settings.MANDRILL_TRACKING_DOMAIN
		MANDRILL_SUBACCOUNT = settings.MANDRILL_SUBACCOUNT
		mandrill_available = True
	except AttributeError:
		mandrill_available = False

	if mandrill_available:
		try:
			return mandrill.Mandrill(MANDRILL_API_KEY)
		except:
			return None
	else:
		return None

def create_mandrill_message(mandrill_client, subject, body, recipients, bcc, attachments=[], reply_to=None):
	"""
	Creates a valid Mandrill message, which can then be sent via their API
	TODO: Handle attachments
	"""
	message = {
		'attachments': attachments,
		'auto_html': None,
		'auto_text': True,
		'bcc_address': ','.join(bcc) if bcc else '',
		'from_email': settings.DEFAULT_FROM_EMAIL,
		'from_name': settings.PROJECT_SITE_NAME,
		'global_merge_vars': [],
		'google_analytics_campaign': '',
		#'google_analytics_domains': [settings.MANDRILL_TRACKING_DOMAIN],
		'headers': {'Reply-To': reply_to if reply_to else settings.DEFAULT_FROM_EMAIL},
		'html': body,
		'images': [],
		'important': False,
		'inline_css': True,
		'merge': False,
		'merge_vars': [],
		'metadata': {},
		'preserve_recipients': None,
		'recipient_metadata': [],
		'return_path_domain': settings.MANDRILL_TRACKING_DOMAIN,
		'signing_domain': settings.MANDRILL_TRACKING_DOMAIN,
		'subaccount': settings.MANDRILL_SUBACCOUNT,
		'subject': subject,
		'tags': [],
		'text': None,
		'to': [{'email':r} for r in recipients],
		'track_clicks': True,
		'track_opens': True,
		#'tracking_domain': settings.MANDRILL_TRACKING_DOMAIN,
		'url_strip_qs': True,
		'view_content_link': None
	}

	return message

def send_mandrill_email(mandrill_client, subject, body, recipients, bcc, attachments=[], content_subtype='html', reply_to=None):
	"""
	Sends a Mandrill API email. If it fails, it will fallback to a standard email.
	"""
	try:
		mandrill_message = create_mandrill_message(mandrill_client, subject, body, recipients, bcc, attachments=attachments, reply_to=reply_to)
		result = mandrill_client.messages.send(message=mandrill_message, async=False)
	except mandrill.Error, e:
		mail_admins('Error sending email via Mandrill API', 'A mandrill error occurred: %s - %s' % (e.__class__, e))
		msg = create_email(subject, body, recipients, bcc, attachments=attachments, content_subtype=content_subtype, reply_to=reply_to)
		msg.send()

# ------------------------------
# GENERIC
# ------------------------------
def formatExceptionInfo(maxTBlevel=5):
	cla, exc, trbk = sys.exc_info()
	excName = cla.__name__
	try:
		excArgs = exc.__dict__["args"]
	except KeyError:
		excArgs = "<no args>"
	excTb = traceback.format_tb(trbk, maxTBlevel)
	return (excName, excArgs, excTb)

# ------------------------------
# EMAIL
# ------------------------------
def create_email(subject, body, recipients, bcc, attachments=[], content_subtype='html'):
	"""
	To add files (i.e. via your form):

	files = []
	files.append({
		'name': request.FILES['attachment'].name,
		'content': request.FILES['attachment'].read(),
		'type': request.FILES['attachment'].content_type
	})
	
	"""
	msg = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, bcc)

	if attachments:
		for attachment in attachments:
			msg.attach(attachment['name'], attachment['content'], attachment['type'])

	if content_subtype:
		msg.content_subtype = content_subtype
	return msg

def send_threaded_email(msg, **kwargs):
	msg.send()

def create_threaded_email(request, subject, body, recipients, template=None, template_context=None, attachments=[], content_subtype='html', bcc=[]):
	"""
	Sends a threaded email. If template is supplied it will load the content from the template, if not 'body' is used.
	"""
	if template:
		site = Site.objects.get_current()
		body = render_to_string(template, Context(dict(template_context, site=site)))

	msg = create_email(subject, body, recipients, bcc=bcc, attachments=attachments, content_subtype=content_subtype)

	t = threading.Thread(target=send_threaded_email, args=[msg], kwargs={'fail_silently': True})
	t.setDaemon(True)
	t.start()

def send_email(subject, body, recipients, bcc, attachments=None, attachment_content_type=None, reply_to=None):
	# Do we want to send this via the Mandrill API?
	mandrill_client = get_mandrill_client()
	if mandrill_client:
		send_mandrill_email(mandrill_client, subject, body, recipients, bcc, reply_to=reply_to)
	else:
		msg = create_email(subject, body, recipients, bcc, attachments=attachments)
		msg.send()

def send_templated_email(template, ctx_dict, subject, recipients, bcc, attachments=None, content_subtype='html', reply_to=None):
	site = Site.objects.get_current()
	body = render_to_string(template, Context(dict(ctx_dict, site=site)))

	# Do we want to send this via the Mandrill API?
	mandrill_client = get_mandrill_client()
	if mandrill_client:
		send_mandrill_email(mandrill_client, subject, body, recipients, bcc, attachments=attachments, content_subtype=content_subtype, reply_to=reply_to)
	else:
		msg = create_email(subject, body, recipients, bcc, attachments=attachments, content_subtype=content_subtype)
		msg.send()
