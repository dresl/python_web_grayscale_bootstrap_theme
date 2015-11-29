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
            form_email = request.POST.get('email')
            form_message = request.POST.get('message')
            form_full_name = request.POST.get('full_name')
            
            subject = 'Site contact form'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, 'resldominik@gymnachod.cz']
            contact_message = "%s: %s via %s" % (
                form_full_name,
                form_message,
                form_email)

            send_mail(subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=True)
            return HttpResponseRedirect('/contact/thanks/')
    else:
        if request.method == 'POST':
            form_email = request.POST.get('email')
            form_message = request.POST.get('message')
            form_full_name = request.POST.get('full_name')
            
            subject = 'Site contact form'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, 'resldominik@gymnachod.cz']
            contact_message = "%s: %s via %s" % (
                form_full_name,
                form_message,
                form_email)

            send_mail(subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=True)
            return HttpResponseRedirect('/contact/thanks/')

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
