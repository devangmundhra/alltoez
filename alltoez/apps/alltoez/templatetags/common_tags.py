from django import template
from django.core.paginator import Paginator, InvalidPage
from django.template.loader import get_template
from django.template.base import TemplateSyntaxError
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
from django.conf import settings
from django.utils.encoding import force_unicode
from django.contrib.admin.util import NestedObjects
from django.utils.safestring import mark_safe
from django.db import router

from HTMLParser import HTMLParser, HTMLParseError

import datetime, re

register = template.Library()

"""
	STRING MANIPULATION AND COMPARISON METHODS
"""
@register.filter(name='split')
def do_split(string, separator=None):
	lst = string.split(separator) if separator else string.split()
	return map(lambda x: x.strip(), lst)

@register.filter
def contains(value, arg):
	"""
	Usage: {% if link_url|contains:"http://www.youtube.com/" %}...
	"""
	return arg in str(value)

def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))
remove_newlines.is_safe = True
remove_newlines = stringfilter(remove_newlines)
register.filter(remove_newlines)

def truncate_chars(s, num):
	"""
	Template filter to truncate a string to at most num characters respecting word
	boundaries.
	"""
	s = force_unicode(s)
	length = int(num)
	if len(s) > length:
		length = length - 3
		if s[length-1] == ' ' or s[length] == ' ':
			s = s[:length].strip()
		else:
			words = s[:length].split()
			if len(words) > 1:
				del words[-1]
			s = u' '.join(words)
		s += '...'
	return s
truncate_chars = allow_lazy(truncate_chars, unicode)

@register.filter
@stringfilter
def truncatechars(value, arg):
	"""
	Truncates a string after a certain number of characters, but respects word boundaries.

	Argument: Number of characters to truncate after.
	"""
	try:
		length = int(arg)
	except ValueError: # If the argument is not a valid integer.
		return value # Fail silently.
	return truncate_chars(value, length)
truncatechars.is_safe = True

"""
	FORM HELPERS
"""
@register.inclusion_tag('helpers/tabular_formset.html')
def render_tabular_formset(formset, add_another=True):
	return {'formset':formset, 'add_another': add_another}

@register.inclusion_tag('helpers/form.html', takes_context=True)
def render_form(context, form):
	context['form'] = form
	return context

@register.filter('field_type')
def field_type(ob):
	return ob.__class__.__name__

class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')
@register.filter
def add_class(value, css_class):
	"""
	Applies a class to any html element, not just input elements!
	"""
	string = unicode(value)
	match = class_re.search(string)
	if match:
		m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
													css_class, css_class),
													match.group(1))
		if not m:
			return mark_safe(class_re.sub(match.group(1) + " " + css_class,
										  string))
	else:
		return mark_safe(string.replace('>', ' class="%s">' % css_class))
	return value

# placeholder_re = re.compile(r'(?<=placeholder=["\'])(.*)(?=["\'])')
# @register.filter
# def label_as_placeholder(input):
#     """Applies a placeholder to any html element based on the label
#     """
#     string = unicode(input)
#     match = placeholder_re.search(string)
#     label_val = input.label.capitalize()
#     if match:
#         m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (label_val, label_val,
#         											label_val, label_val),
#         											match.group(1))
#         if not m:
#             return mark_safe(placeholder_re.sub(match.group(1) + " " + label_val,
#         								  string))
#     else:
#         return mark_safe(string.replace('>', ' placeholder="%s">' % label_val))
#     return input

class RecurseNode(template.Node):
	def __init__(self, var, name, child, nodeList):
		self.var = var
		self.name = name
		self.child = child
		self.nodeList = nodeList

	def __repr__(self):
		return '<RecurseNode>'

	def renderCallback(self, context, vals, level):
		output = []
		try:
			if len(vals):
				pass
		except:
			vals = [vals]
		if len(vals):
			if 'loop' in self.nodeList:
				output.append(self.nodeList['loop'].render(context))
			for val in vals:
				context.push()
				context['level'] = level
				context[self.name] = val
				if 'child' in self.nodeList:
					output.append(self.nodeList['child'].render(context))
					child = self.child.resolve(context)
					if child:
						output.append(self.renderCallback(context, child, level + 1))
				if 'endloop' in self.nodeList:
					output.append(self.nodeList['endloop'].render(context))
				else:
					output.append(self.nodeList['endrecurse'].render(context))
				context.pop()
			if 'endloop' in self.nodeList:
				output.append(self.nodeList['endrecurse'].render(context))
		return ''.join(output)

	def render(self, context):
		vals = self.var.resolve(context)
		output = self.renderCallback(context, vals, 1)
		return output

def do_recurse(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 6 and bits[2] != 'with' and bits[4] != 'as':
		raise template.TemplateSyntaxError, "Invalid tag syxtax expected '{% recurse [childVar] with [parents] as [parent] %}'"
	child = parser.compile_filter(bits[1])
	var = parser.compile_filter(bits[3])
	name = bits[5]

	nodeList = {}
	while len(nodeList) < 4:
		temp = parser.parse(('child','loop','endloop','endrecurse'))
		tag = parser.tokens[0].contents
		nodeList[tag] = temp
		parser.delete_first_token()
		if tag == 'endrecurse':
			break

	return RecurseNode(var, name, child, nodeList)
do_recurse = register.tag('recurse', do_recurse)


@register.simple_tag
def active(request, pattern, exclude=None):
	import re
	if re.search(pattern, request.path) and (not exclude or not re.search(exclude, request.path)):
		return 'active'
	return ''


@register.filter()
def is_today(date):
	today = datetime.date.today()
	dtype = type(date)
	if dtype == datetime.date:
		return date == today
	elif dtype == datetime.datetime:
		return date.date() == today

	return ''

@register.filter(name='range')
def do_range(x, y=None):
	if y != None:
		return range(x,y)
	return range(x)

@register.inclusion_tag('helpers/deleted_objects.html')
def list_deleted_objects(obj):
	model = obj.__class__
	def format_callback(item):
		return u'%s: %s' % (item._meta.verbose_name.capitalize(), force_unicode(item))

	collector = NestedObjects(using=router.db_for_write(model))
	collector.collect(model.objects.filter(id=obj.id))
	to_delete = collector.nested(format_callback)

	return {'to_delete': to_delete}

@register.filter()
def mod(x, y):
	return x % y

@register.filter()
def subtract(value, arg):
	return value - arg

@register.filter(name='dir')
def do_dir(object):
	return dir(object)

@register.filter
def lookup(l, key):
    return l[key]

@register.filter
def url_target_blank(text):
	return text.replace('<a ', '<a target="_blank" ')
url_target_blank.is_safe = True

@register.simple_tag
def time_of_day():
	import datetime, pytz
	from django.conf import settings
	cur_time = datetime.datetime.now(tz=pytz.timezone(str(settings.TIME_ZONE)))
	if cur_time.hour < 12:
		return 'Morning'
	elif 12 <= cur_time.hour < 18:
		return 'Afternoon'
	else:
		return 'Evening'

@register.filter
@stringfilter
def retaintags(value, tags):
	"""Retains the tags passed and strips out all others from the output.
	i.e. {{ value|retaintags:"b i" }} will retain just b and i tags
	"""
	#from django.utils.html import remove_tags
	#return remove_tags(value, tags)

	import re
	tags_re = u'(%s)' % u'|'.join(tags)
	striptags_re = re.compile(ur'</(?!{0}).*?>|<(?!/)(?!{0}).*?>'.format(tags_re), re.U)
	striptags_re.sub(u'', value)
	return mark_safe(value)


@register.filter
def order_by(l, key):
	return sorted(l, key=lambda k: k[key])


@register.filter
def youtubize(text):
	#<a target="_blank" href="https://www.youtube.com/watch?v=-7jS7X-2ggA" rel="nofollow">https://www.youtube.com/watch?v=-7jS7X-2ggA</a>
	regex = re.compile(r'(<a\starget="_blank"\shref="(http://|https://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})"\srel="nofollow">(http://|https://)?(www\.)?(youtube\.com/watch\?v=)?([A-Za-z0-9\-=_]{11})</a>)')
	matches = regex.findall(text)
	if not matches:
		return text

	for match in matches:
		text = text.replace(match[0], """
			<iframe class="youtube-embeded" width="100%%"
			height="250px" src="//www.youtube.com/embed/%s?wmode=transparent"
			frameborder="0" wmode="Opaque" allowfullscreen></iframe>
	    """ % match[4])
	return text
youtubize.is_safe = True # Don't escape HTML


@register.filter("urlize_html")
def urlize_html(html):
	"""
    Returns urls found in an (X)HTML text node element as urls via Django urlize filter.
    """

	try:
		from BeautifulSoup import BeautifulSoup
		from django.utils.html import urlize
	except ImportError:
		if settings.DEBUG:
			raise TemplateSyntaxError, "Error in urlize_html The Python BeautifulSoup libraries aren't installed."
		return html
	else:
		soup = BeautifulSoup(html)

		textNodes = soup.findAll(text=True)
		for textNode in textNodes:
			urlizedText = urlize(textNode, nofollow=True)
			textNode.replaceWith(urlizedText)

		return str(soup).replace('&lt;', '<').replace('&gt;', '>')

@register.filter()
def get_keys(dict):
    return dict.keys()

@register.simple_tag
def url_replace(request, field, value):
    """
    Replace a get parameter in a url
    :param request:
    :param field:
    :param value:
    :return:
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()