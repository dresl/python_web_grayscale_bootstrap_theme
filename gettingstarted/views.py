from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Greeting, Sidebar
from books.models import Publisher, Author, Book
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.core.mail import send_mail,BadHeaderError
from forms import ContactForm
from django.conf import settings
from django.contrib.auth.models import User

def contact_thanks(request):
    args = {}
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        return render(request, 'apps/contact_thanks.html', args)
    else:
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'apps/contact_thanks.html', args)

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if request.user.is_authenticated():
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['resldominik@gymnachod.cz'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return render(request,'apps/new_contact_form.html',{'username': request.user.username,
                                                                'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['resldominik@gymnachod.cz'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return render(request,'apps/new_contact_form.html',)

def contact(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if not request.POST.get('subject', '') and not request.POST.get('message', '') or request.POST.get('email') and '@' not in request.POST['email']:
                subject_error = 'Enter a subject.'
                message_error = 'Enter a message.'
                email_error = 'Enter a valid e-mail address.'
                return render(request, 'apps/contact_form.html', {'subject_error': subject_error, 
                                                                  'message_error': message_error,
                                                                  'email_error': email_error,
                                                                  'username': request.user.username,
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if not request.POST.get('subject', ''):
                subject_error = 'Enter a subject.'
                return render(request, 'apps/contact_form.html', {'subject_error': subject_error,'username': request.user.username,
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if not request.POST.get('message', ''):
                message_error = 'Enter a message.'
                return render(request, 'apps/contact_form.html', {'message_error': message_error,'username': request.user.username,
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if request.POST.get('email') and '@' not in request.POST['email']:
                email_error = 'Enter a valid e-mail address.'
                return render(request, 'apps/contact_form.html', {'email_error': email_error,'username': request.user.username,
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            else:
                send_mail(
                    request.POST['subject'],
                    request.POST['message'],
                    request.POST.get('email', ''),
                    ['resldominik@gymnachod.cz'], fail_silently=False
                )
                return HttpResponseRedirect('/contact/thanks/')
        return render(request,'apps/contact_form.html', {
            'subject': request.POST.get('subject', ''),
            'message': request.POST.get('message', ''),
            'email': request.POST.get('email', ''),
            'username': request.user.username,
            'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
            'full_name': request.user.first_name + ' ' + request.user.last_name
        })
    else:
        if request.method == 'POST':
            if not request.POST.get('subject', '') and not request.POST.get('message', '') or request.POST.get('email') and '@' not in request.POST['email']:
                subject_error = 'Enter a subject.'
                message_error = 'Enter a message.'
                email_error = 'Enter a valid e-mail address.'
                return render(request, 'apps/contact_form.html', {'subject_error': subject_error, 
                                                                  'message_error': message_error,
                                                                  'email_error': email_error,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if not request.POST.get('subject', ''):
                subject_error = 'Enter a subject.'
                return render(request, 'apps/contact_form.html', {'subject_error': subject_error,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if not request.POST.get('message', ''):
                message_error = 'Enter a message.'
                return render(request, 'apps/contact_form.html', {'message_error': message_error,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            if request.POST.get('email') and '@' not in request.POST['email']:
                email_error = 'Enter a valid e-mail address.'
                return render(request, 'apps/contact_form.html', {'email_error': email_error,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
            else:
                send_mail(
                    request.POST['subject'],
                    request.POST['message'],
                    request.POST.get('email', ''),
                    ['resldominik@gymnachod.cz'], fail_silently=False
                )
                return HttpResponseRedirect('/contact/thanks/')
        return render(request,'apps/contact_form.html', {
            'subject': request.POST.get('subject', ''),
            'message': request.POST.get('message', ''),
            'email': request.POST.get('email', ''),
            'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        })

def home(request):
    now = datetime.datetime.now()
    path = request.path
    your_browser = request.META.get('HTTP_USER_AGENT', 'unknown')
    if request.user.is_authenticated():
        return render(request, 'apps/current.html', {'current_date': now, 'path': path, 
                                                     'your_browser': your_browser,
                                                     'username': request.user.username,
                                                     'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
                                                     'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'apps/current.html', {'current_date': now, 'path': path, 
                                                     'your_browser': your_browser,
                                                     'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})

def search_form(request):
    args = {}
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        return render(request, 'apps/search_form.html', args)
    else:
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'apps/search_form.html', args)

def search(request):
    errors = []
    if request.user.is_authenticated():
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                errors.append('Enter a search term.')
            elif len(q) > 20:
                errors.append('Please enter at most 20 characters.')
            else:
                books = Book.objects.filter(title__icontains=q)
                return render(request, 'apps/search_results.html', {'books': books, 'query': q, 'username': request.user.username,
                                                                    'full_name': request.user.first_name + ' ' + request.user.last_name,
                                                                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]})
        return render(request, 'apps/search_form.html', {'errors': errors, 'username': request.user.username,
                                                         'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
                                                         'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
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
    if request.user.is_authenticated():
        return render(request, 'apps/future.html', {'next_time': futuretime, 
                                                    'hour_offset': offset,
                                                    'path': path,
                                                    'username': request.user.username,
                                                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'),
                                                    'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'apps/future.html', {'next_time': futuretime, 
                                                    'hour_offset': offset,
                                                    'path': path,
                                                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')})
        