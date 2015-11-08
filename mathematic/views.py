from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.template import RequestContext
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.template import Context
import datetime
from polls.models import Choice, Question, Greeting, Sidebar
from books.models import Book
from mathematic.models import Brigade, Day
from django.core.mail import send_mail
from django.conf import settings
from mathematic.forms import BrigadeForm

def index(request):
    args={}
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        return render(request, 'mathematic/mathindex.html', args)
    else:
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]
        return render(request, 'mathematic/mathindex.html', args)

def create(request):
    
    if request.POST:
        form = BrigadeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/math/brigade/')
    else:
        form = BrigadeForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['brigade'] = Day.objects.order_by('-pub_date')[:1]
    args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['form'] = args['form']
        return render(request, 'mathematic/brigade_create.html', args)
    else:
        return render(request, 'mathematic/brigade_create.html', args)

class BrigadeIndexView(generic.ListView):
    template_name = 'mathematic/brigade_index.html'
    context_object_name = 'latest_brigade_list'

    def get_context_data(self, *args, **kwargs):
        
        context = super(BrigadeIndexView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated():
            context['full_name'] = self.request.user.first_name + ' ' + self.request.user.last_name
            context['username'] = self.request.user.username
        return context

    def get_queryset(self):
        """
        Excludes any Brigades that aren't published yet.
        """
        return Brigade.objects.filter(pub_date__lte=timezone.now())

def DetailView(request, pk):
    title_brigade = Brigade.objects.get(id=pk)
    if request.user.is_authenticated():
        brigade = Day.objects.filter(brigade__pk=pk).order_by('pub_date')
        def sum_hours(hours):
            total = 0
            for item in hours:
                total += item.hours_per_day
            return total
        sum_hours = sum_hours(brigade)

        if sum_hours > 0:
            def average_hours(hours):
                total = 0
                average = 0
                for item in hours:
                    total += item.hours_per_day
                    if len(str(item.hours_per_day)) == 2:
                        a = len(str(item.hours_per_day)) - 1
                        average += a
                    else:
                        average += len(str(item.hours_per_day))
                    
                total = total / float(average)
                return round(total, 2)
            average_hours = average_hours(brigade)

            def sum_price(hours):
                total = 0
                for item in hours:
                    total += float(item.hours_per_day) * 50
                return total
            sum_price = sum_price(brigade)

            def average_price(hours):
                total = 0
                average = 0
                for item in hours:
                    total += float(item.hours_per_day) * 50
                    if len(str(item.hours_per_day)) == 2:
                        a = len(str(item.hours_per_day)) - 1
                        average += a
                    else:
                        average += len(str(item.hours_per_day))
                total = total / float(average)
                return round(total, 2)
            average_price = average_price(brigade)
            
            return render(request, 'mathematic/brigade_detail.html', {'brigade': brigade,
                                                           'sum_hours': sum_hours,
                                                           'title_brigade': title_brigade,
                                                           'average_hours': average_hours,
                                                           'sum_price': sum_price,
                                                           'average_price': average_price,
                                                           'username': request.user.username,
                                                           'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                           'full_name': request.user.first_name + ' ' + request.user.last_name})
        else:
            return render(request, 'mathematic/brigade_index_error.html')
    
    else:
        brigade = Day.objects.filter(brigade__pk=pk).order_by('pub_date')
        def sum_hours(hours):
            total = 0
            for item in hours:
                total += item.hours_per_day
            return total
        sum_hours = sum_hours(brigade)

        if sum_hours > 0:
            def average_hours(hours):
                total = 0
                average = 0
                for item in hours:
                    total += item.hours_per_day
                    if len(str(item.hours_per_day)) == 2:
                        a = len(str(item.hours_per_day)) - 1
                        average += a
                    else:
                        average += len(str(item.hours_per_day))
                    
                total = total / float(average)
                return round(total, 2)
            average_hours = average_hours(brigade)

            def sum_price(hours):
                total = 0
                for item in hours:
                    total += float(item.hours_per_day) * 50
                return total
            sum_price = sum_price(brigade)

            def average_price(hours):
                total = 0
                average = 0
                for item in hours:
                    total += float(item.hours_per_day) * 50
                    if len(str(item.hours_per_day)) == 2:
                        a = len(str(item.hours_per_day)) - 1
                        average += a
                    else:
                        average += len(str(item.hours_per_day))
                total = total / float(average)
                return round(total, 2)
            average_price = average_price(brigade)

            return render(request, 'mathematic/brigade_detail.html', {'brigade': brigade,
                                                           'sum_hours': sum_hours,
                                                           'average_hours': average_hours,
                                                           'title_brigade': title_brigade,
                                                           'sum_price': sum_price,
                                                           'average_price': average_price,
                                                           'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],})
        else:
            return render(request, 'mathematic/brigade_index_error.html')

class CalcIndexView(generic.ListView):
    template_name = 'mathematic/calc_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CalcIndexView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated():
            context['full_name'] = self.request.user.first_name + ' ' + self.request.user.last_name
            context['username'] = self.request.user.username
        return context

    def get_queryset(self):

        return Brigade.objects.filter(pub_date__lte=timezone.now())

def choose(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST['myfield'] == 'plus':
                myfield = request.POST['myfield']
                return render(request, 'mathematic/calc_index.html', {'myfield': myfield})
            elif request.POST['myfield'] == 'minus':
                myfield = request.POST['myfield']
                return render(request, 'mathematic/calc_index.html', {'myfield': myfield})
    else:
        if request.method == 'POST':
            if request.POST['myfield'] == 'plus':
                myfield = request.POST['myfield']
                return render(request, 'mathematic/calc_index.html', {'myfield': myfield})
            elif request.POST['myfield'] == 'minus':
                myfield = request.POST['myfield']
                return render(request, 'mathematic/calc_index.html', {'myfield': myfield})

def count(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST['myfield'] == 'plus':
                if len(request.POST['cislo1']) == 0 or len(request.POST['cislo2']) == 0:
                    error_message = 'Zadej vsechny udaje'
                    return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                                   'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
                elif request.POST['cislo1'].isdigit() and request.POST['cislo2'].isdigit():
                    cislo1 = int(request.POST['cislo1'])
                    cislo2 = int(request.POST['cislo2'])
                    vysledek = cislo2 + cislo1
                    return render(request, 'mathematic/vysledek.html', {'vysledek': vysledek,'username': request.user.username,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name})
                elif not request.POST['cislo1'].isdigit() or not request.POST['cislo2'].isdigit():
                    error_message = 'Musis zadat cislo'
                    return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                                   'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
            elif request.POST['myfield'] == 'minus':
                if len(request.POST['cislo1m']) == 0 or len(request.POST['cislo2m']) == 0:
                    error_message = 'Zadej vsechny udaje'
                    return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                                   'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
                elif request.POST['cislo1m'].isdigit() and request.POST['cislo2m'].isdigit():
                    cislo1 = int(request.POST['cislo1m'])
                    cislo2 = int(request.POST['cislo2m'])
                    vysledek = cislo1 - cislo2
                    return render(request, 'mathematic/vysledek.html', {'vysledek': vysledek,'username': request.user.username,
                                                                  'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                  'full_name': request.user.first_name + ' ' + request.user.last_name})
                elif not request.POST['cislo1m'].isdigit() or not request.POST['cislo2m'].isdigit():
                    error_message = 'Musis zadat cislo'
                    return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                                   'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
            else:
                error_message = 'ahoj'
                return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                               'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                               'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        if request.method == 'POST':
            if len(request.POST['cislo1']) == 0 or len(request.POST['cislo2']) == 0:
                error_message = 'Zadej vsechny udaje'
                return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                               'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]})
            elif request.POST['cislo1'].isdigit() and request.POST['cislo2'].isdigit():
                cislo1 = int(request.POST['cislo1'])
                cislo2 = int(request.POST['cislo2'])
                vysledek = cislo2 + cislo1
                return render(request, 'mathematic/vysledek.html', {'vysledek': vysledek,'username': request.user.username,
                                                              'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]})
            elif not request.POST['cislo1'].isdigit() or not request.POST['cislo2'].isdigit():
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                               'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]})
            else:
                error_message = 'ahoj'
                return render(request, 'mathematic/mathindex.html', {'error_message': error_message,'username': request.user.username,
                                                               'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]})