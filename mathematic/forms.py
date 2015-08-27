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
