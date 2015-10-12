from django import forms
from blog.models import Blog
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BlogForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
                super(BlogForm, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_id = 'id-exampleForm'
                self.helper.form_method = 'post'
                self.helper.form_action = 'blog_create'
                self.helper.form_class = 'form-horizontal'
                self.helper.label_class = 'col-lg-2'
                self.helper.field_class = 'col-lg-8'
                self.helper.layout = Layout(
                    'email',
                    'password',
                    'remember_me',
                    StrictButton('Sign in', css_class='btn-default'),
                )

                self.helper.add_input(Submit('submit', 'Submit'))