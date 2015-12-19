from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Sidebar
from books.models import Publisher, Author, Book
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.core.mail import send_mail,BadHeaderError
from django.template.loader import render_to_string
from forms import ContactForm
from django.conf import settings
from django.contrib.auth.models import User

def contact_thanks(request):
    args = {}
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'apps/contact_thanks.html', args)

def send_email(request):
    form_full_name = request.POST.get('full_name')
    form_message = request.POST.get('message')
    form_from_email = request.POST.get('email')
    msg_plain = render_to_string('apps/email.txt', {
        'form_from_email': form_from_email,
        'form_message': form_message,
        'form_full_name': form_full_name })
    msg_html = render_to_string('apps/email.html', {
        'form_from_email': form_from_email,
        'form_message': form_message,
        'form_full_name': form_full_name })
    if form_full_name and form_message and form_from_email:
        try:
            send_mail('DjangoSite', msg_plain, form_from_email, \
                ['nikicresl@gmail.com'], html_message=msg_html, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return render(request,'apps/new_contact_form.html',)

def home(request):
    now = datetime.datetime.now()
    path = request.path
    your_browser = request.META.get('HTTP_USER_AGENT', 'unknown')
    return render(request, 'apps/current.html', {
        'current_date': now, 'path': path, 
        'your_browser': your_browser,
        'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})

def search_form(request):
    args = {}
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'apps/search_form.html', args)

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        args = {}
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            args['books'] = Book.objects.filter(title__icontains=q)
            args['query'] = q
            args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
            return render(request, 'apps/search_results.html', args)
    return render(request, 'apps/search_form.html', {'errors': errors, 'username': request.user.username,
                                                     'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    futuretime = datetime.datetime.now() + datetime.timedelta(hours=offset)
    path = request.path
    return render(request, 'apps/future.html', {'next_time': futuretime, 
                                                'hour_offset': offset,
                                                'path': path,
                                                'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
