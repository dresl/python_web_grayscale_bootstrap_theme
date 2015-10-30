from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Greeting, Sidebar
from userprofile.models import UserProfile
from books.models import Publisher, Author, Book
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from userprofile.forms import MyRegistrationForm, UserProfileForm
import datetime
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django.contrib.auth.models import User

def edit_profile(request):
    if request.POST:
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = UserProfileForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['form'] = args['form']
        return render(request, 'userprofile/edit_profile.html', args)
    else:
        return render(request, 'userprofile/edit_profile.html', args)

def userprofile(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
    	args['profile_picture'] = request.user.profile.profile_picture
        args['hobbies'] = request.user.profile.hobbies
        args['greetings'] = Greeting.objects.all()
        args['questions'] = Question.objects.all()
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        return render(request,'userprofile/profile.html', args)
    else:
        args['greetings'] = Greeting.objects.all()
        args['questions'] = Question.objects.all()
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'userprofile/profile.html', args)

def login(request):
    c = {}
    c.update(csrf(request))
    c['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'userprofile/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/profile/')
    else:
        return HttpResponseRedirect('/accounts/invalid/')

def loggedin(request):
    args = {}
    if request.user.is_authenticated():
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['username'] = request.user.username
        return render(request, 'userprofile/loggedin.html', args)
    else:
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'userprofile/loggedin.html', args)

def invalid_login(request):
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request,'userprofile/invalid_login.html', {'sidebar': sidebar})

def logout(request):
    auth.logout(request)
    args = {}
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'userprofile/logout.html', args)

def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success/')
        else:
            return HttpResponseRedirect('/accounts/register/')

    args = {}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request,'userprofile/register.html', args)

def register_success(request):
    return render(request, 'userprofile/register_success.html')