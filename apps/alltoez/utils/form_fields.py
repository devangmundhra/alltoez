from django import forms
import dateutil.parser as dateparser

class MultiSelectFormField(forms.MultipleChoiceField):
	widget = forms.CheckboxSelectMultiple
	
	def __init__(self, *args, **kwargs):
		self.max_choices = kwargs.pop('max_choices', 0)
		super(MultiSelectFormField, self).__init__(*args, **kwargs)

	def clean(self, value):
		if not value and self.required:
			raise forms.ValidationError(self.error_messages['required'])
		if value and self.max_choices and len(value) > self.max_choices:
			raise forms.ValidationError('You must select a maximum of %s choice%s.'
					% (apnumber(self.max_choices), pluralize(self.max_choices)))
		return value


class MultipleDynamicChoiceField(forms.MultipleChoiceField):
	def clean(self, value):
		return value
	   
class DateTimeParserField(forms.DateTimeField):
	def prepare_value(self, value):
		return value
	
	def to_python(self, value):
		try:
			return dateparser.parse(value, dayfirst=True)
		except ValueError, AttributeError:
			raise ValidationError(self.error_messages['invalid'])

	def strptime(self, value, format):
		return datetime.datetime.strptime(value, format)
	