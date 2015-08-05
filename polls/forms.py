from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, ButtonHolder, Field, Fieldset, Layout,
                                 Submit)
from django import forms
from polls.models import Greeting


class GreetingForm(forms.ModelForm):

    class Meta:
        model = Greeting
        fields = ('title', 'body', 'pub_date', 'thumbnail')

    def __init__(self, *args, **kwargs):
        super(GreetingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Main',
                'title',
                'body',
                'pub_date',
                'thumbnail'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
