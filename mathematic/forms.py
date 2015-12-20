from django import forms
from mathematic.models import Brigade, Day

class BrigadeForm(forms.ModelForm):

	class Meta:
		model = Brigade
		fields = ('brigade_title', 'owner', 'rate', 'pub_date')
