from django import forms
from mathematic.models import Brigade, Day

class BrigadeForm(forms.ModelForm):

	class Meta:
		model = Day
		fields = ('brigade', 'number_of_day', 'hours_per_day', 'pub_date')
	