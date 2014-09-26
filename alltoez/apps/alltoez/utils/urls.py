from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve, Resolver404

def join_url(domain, url):
	cleaned_domain = domain[:-1] if domain[-1] == '/' else domain
	cleaned_url = url[1:] if url[0] == '/' else url
	return '%s/%s' % (cleaned_domain, cleaned_url)

def validate_unique_resolve(path):
	uniqueurl = False
	try:
		resolve(path)
	except Resolver404:
		uniqueurl = True

	return uniqueurl

def validate_unique_resolve_return_resolver(path):
	resolver = None
	try:
		resolver = resolve(path)
	except Resolver404:
		resolver = None

	return resolver