from itertools import chain
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django import forms
from django.db.models import get_model
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.conf import settings

from PIL import Image

import os

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

   items_per_row = 4 # Number of items per row

   def render(self, name, value, attrs=None, choices=()):
       if value is None: value = []
       has_id = attrs and 'id' in attrs
       final_attrs = self.build_attrs(attrs, name=name)
       output = ['<table><tr>']
       # Normalize to strings
       str_values = set([force_unicode(v) for v in value])
       for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
           # If an ID attribute was given, add a numeric index as a suffix,
           # so that the checkboxes don't all have the same ID attribute.
           if has_id:
               final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
               label_for = ' for="%s"' % final_attrs['id']
           else:
               label_for = ''

           cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
           option_value = force_unicode(option_value)
           rendered_cb = cb.render(name, option_value)
           option_label = conditional_escape(force_unicode(option_label))
           if i != 0 and i % self.items_per_row == 0:
               output.append('</tr><tr>')
           output.append('<td nowrap><label%s>%s %s</label></td>' % (label_for, rendered_cb, option_label))
       output.append('</tr></table>')
       return mark_safe('\n'.join(output))

class FileBrowserFrontendWidget(forms.FileInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        return render_to_string("filebrowser/custom_field_frontend.html", locals())
