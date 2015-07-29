from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse
from django.views import generic
from django.views.generic.base import TemplateView
from hello.models import Greeting
from django.template.loader import get_template
from django.template import Context
import os

# class index(request):
    # times = int(os.environ.get('TIMES',3))
    # return HttpResponse('Hello! ' * times)

class HelloName(TemplateView):

	template_name = 'hello/name.html'

	def get_context(self, **kwargs):
		context = super(HelloName, self).get_context(**kwargs)
		context['name'] = 'Dominik'
		return context

def db(request):
	a = "Dominik"
	return render_to_response('hello/dbnew.html', {'a': a})

def basehtml(request):
	return render_to_response('hello/base.html')

def greetings(request):
	myname = "Dominik"
	x = "How are you"
	a = "-".join(x.split())
	t = a.lower()
	return render_to_response('hello/greetings.html', {'greetings': Greeting.objects.all(), 'myname': myname, 'x': t })

def greeting(request, greeting_id=1):
	return render_to_response('hello/greetingdetail.html', {'greeting': Greeting.objects.get(id=greeting_id) })