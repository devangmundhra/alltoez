from django import forms

def get_fieldsets_attr(sets, cache_attr='_fieldsets'):
	"""
	Get a form attribute for getting groups of (bound) fields.

		class MyForm(forms.Form):
			first_name = forms.Charfield()
			last_name = forms.Charfield()
			email = forms.Charfield()
			phone = forms.Charfield()

			SETS = {
				'': ('title', 'description', 'photo', 'external_link'),
				'Location': ('location', 'postcode', 'address', 'country')
			}
			fieldsets = get_fieldsets_attr(sets=SETS)

	This is specially usefull in templates:

		{% for fieldset in form.fieldsets %}
			<fieldset>
				{% if fieldset.name %}<legend><b>{{fieldset.name}}</b></legend>{% endif %}
				{% for field in fieldset.fields %}
					{{field}}
				{% endfor %}
			</fieldset>
		{% endfor %}
	"""
	def inner(self):
		if not hasattr(self, cache_attr):
			from django.forms.forms import BoundField
			fieldsets = []
			for item in sets:
				fieldset = {}
				fieldset['title'] = item['title']
				fieldset['description'] = item['description'] if 'description' in item else ''
				fieldset['fields'] = []
				fieldset['span'] = item.get('span', None)

				for fieldname in item['fields']:
					fieldset['fields'].append(BoundField(self, self.fields[fieldname], fieldname))

				fieldsets.append(fieldset)

			self.cache_attr = fieldsets
		return self.cache_attr
	return inner

