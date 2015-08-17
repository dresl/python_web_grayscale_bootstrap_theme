from django import forms
from mathematic.models import Brigade, Day

from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, ButtonHolder, Field, Fieldset, Layout,
                                 Submit)

class BrigadeForm(forms.Form):

	class Meta:
		model = Day
		fields = ('brigade', 'number_of_day', 'hours_per_day', 'pub_date')

	def __init__(self, *args, **kwargs):
     	super(BrigadeForm, self).__init__(*args, **kwargs)
     	self.helper = FormHelper()
     	self.helper.layout = Layout(
        Fieldset(
            'Main',
            'brigade',
            'number_of_day',
            'hours_per_day',
            'pub_date'
        ),
        ButtonHolder(
            Submit('submit', 'Submit', css_class='button white')
        )
     )
