from django import forms
from polls.models import Greeting

class GreetingForm(forms.ModelForm):

	class Meta:
		model = Greeting
		fields = ('title', 'body', 'pub_date', 'thumbnail')