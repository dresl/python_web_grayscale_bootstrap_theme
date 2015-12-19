# encoding: utf-8
from django.shortcuts import get_object_or_404, render, render_to_response
from math import *
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
from polls.models import Choice, Question, Sidebar
from books.models import Book
from mathematic.models import Brigade, Day
from django.core.mail import send_mail
from django.conf import settings
from mathematic.forms import BrigadeForm

def index(request):
    args={}
    args['sidebar'] = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')[:50]
    return render(request, 'mathematic/mathindex.html', args)

def index_create_brigade(request):
    args = {}
    args['brigades'] = Brigade.objects.all()
    args['now'] = str(timezone.now().year) + '-' + str(datetime.datetime.now().month) + '-' + \
        str(timezone.now().day) + ' ' + str(timezone.now().hour) + ':' + \
        str(timezone.now().minute) + ':' + str(timezone.now().second)
    args['username'] = request.user.username
    return render(request, 'mathematic/brigade_create.html', args)

def create_brigade(request):
    brigade_title = request.POST['brigade_title']
    rate = request.POST['rate']
    now = request.POST['now']
    a = Brigade(brigade_title=brigade_title, rate=rate, pub_date=now)
    a.save()
    return HttpResponseRedirect('/math/brigade/')

def index_create_day(request):
    args = {}
    list_ = []
    brigades_title = Brigade.objects.all()
    for i in brigades_title:
        q = Brigade.objects.get(brigade_title=i)
        if Day.objects.filter(brigade=q).count() == 0:
            list_.append('%s: Den 0' % (q))
        else:
            last_days = q.day_set.order_by('-pub_date')[0:1].get()
            list_.append('%s: %s' % (q, last_days))
    args['last_days'] = ", ".join(list_)
    args['brigades'] = Brigade.objects.all()
    return render(request, 'mathematic/day_create.html', args)

def create_day(request):
    if request.POST:
        brigade_title = request.POST['brigade_title']
        number_of_day = request.POST['number_of_day']
        hours_per_day = request.POST['hours_per_day']
        now = request.POST['now']
        q = Brigade.objects.get(brigade_title=brigade_title)
        q.day_set.create(number_of_day=number_of_day,
            hours_per_day=hours_per_day, pub_date=now)
        return HttpResponseRedirect('/math/brigade/')

def choose_brigade(request):
    if request.method == 'GET':
        args = {}
        list_ = []
        brigades_title = Brigade.objects.all()
        for i in brigades_title:
            q = Brigade.objects.get(brigade_title=i)
            if Day.objects.filter(brigade=q).count() == 0:
                list_.append('%s: Den 0' % (q))
            else:
                last_days = q.day_set.order_by('-pub_date')[0:1].get()
                list_.append('%s: %s' % (q, last_days))
        args['last_days'] = ", ".join(list_)
        args['brigade'] = request.GET['myfield']
        args['now'] = str(timezone.now().year) + '-' + str(datetime.datetime.now().month) + '-' + \
        str(timezone.now().day) + ' ' + str(timezone.now().hour) + ':' + \
        str(timezone.now().minute) + ':' + str(timezone.now().second)
        a = Brigade.objects.get(brigade_title=args['brigade'])
        if a.day_set.count() == 0:
            last_day = str("Den: 0")[5:len(str("Den: 0"))]
        else:
            last_day_ = a.day_set.all().order_by('-pub_date')[0]
            last_day = str(last_day_)[5:len(str(last_day_))]
        args['last_day'] = int(last_day) + 1
        args['brigades'] = Brigade.objects.all()
        return render(request, 'mathematic/day_create.html', args)


class BrigadeIndexView(generic.ListView):
    template_name = 'mathematic/brigade_index.html'
    context_object_name = 'latest_brigade_list'

    def get_context_data(self, *args, **kwargs):
        
        context = super(BrigadeIndexView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        """
        Excludes any Brigades that aren't published yet.
        """
        return Brigade.objects.filter(pub_date__lte=timezone.now())

def DetailView(request, pk):
    title_brigade = Brigade.objects.get(id=pk)
    rate = str(title_brigade.rate)
    if Day.objects.filter(brigade__pk=pk).count() == 0:
        return render(request, 'mathematic/brigade_detail.html', {})
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
                    total += float(item.hours_per_day) * int(title_brigade.rate)
                return total
            sum_price = sum_price(brigade)

            def average_price(hours):
                total = 0
                average = 0
                for item in hours:
                    total += float(item.hours_per_day) * int(title_brigade.rate)
                    if len(str(item.hours_per_day)) == 2:
                        a = len(str(item.hours_per_day)) - 1
                        average += a
                    else:
                        average += len(str(item.hours_per_day))
                total = total / float(average)
                return round(total, 2)
            average_price = average_price(brigade)

            return render(request, 'mathematic/brigade_detail.html', {
                'brigade': brigade,
                'sum_hours': sum_hours,
                'average_hours': average_hours,
                'title_brigade': title_brigade,
                'sum_price': sum_price,
                'average_price': average_price,
                'rate': rate,
                'sidebar': Sidebar.objects.filter(
                    pub_date__lte=timezone.now()).order_by('-pub_date')[:50],})
        else:
            return render(request, 'mathematic/brigade_index_error.html')

class CalcIndexView(generic.ListView):
    template_name = 'mathematic/calc_index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CalcIndexView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):

        return Brigade.objects.filter(pub_date__lte=timezone.now())

#*************Circle***************************************************************
def index_circle(request):
    return render(request, 'mathematic/index_circle.html',)

def choose_circle(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'rk':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_circle.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'ok':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_circle.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'sk':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_circle.html', {'myfield': myfield})

def count_circle(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'rk':
            if request.GET['cislo1']:
                cislo1_ = float(request.GET['cislo1'])
                cislo1 = str(cislo1_)
                obvod_ = 2*3.14*cislo1_
                obvod = str(obvod_)
                obsah_ = 3.14*pow(cislo1_, 2)
                obsah = str(obsah_)
                return render(request, 'mathematic/index_circle.html', {
                    'cislo1': cislo1, 'obvod': obvod, 'obsah': obsah,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                              })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_circle.html', {
                    'error_message': error_message,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                               })

        elif request.GET['myfield'] == 'ok':
            if request.GET['cislo2']:
                obvod_ = float(request.GET['cislo2'])
                obvod = str(obvod_)
                cislo2_ = obvod_ / (2*3.14)
                cislo2 = str(cislo2_)
                obsah_ = 3.14*pow(cislo2_, 2)
                obsah = str(obsah_)
                return render(request, 'mathematic/index_circle.html', {
                    'cislo2': cislo2, 'obvod': obvod, 'obsah': obsah,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                              })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_circle.html', {
                    'error_message': error_message,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                               })

        elif request.GET['myfield'] == 'sk':
            if request.GET['cislo3']:
                obsah_ = float(request.GET['cislo3'])
                obsah = str(obsah_)
                cislo3_ = sqrt(obsah_/3.14)
                cislo3 = str(cislo3_)
                obvod_ = 2*3.14*cislo3_
                obvod = str(obvod_)
                return render(request, 'mathematic/index_circle.html', {
                    'cislo3': cislo3, 'obvod': obvod, 'obsah': obsah,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                              })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_circle.html', {
                    'error_message': error_message,
                    'sidebar': Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50],
                                                               })

#*************Calc***************************************************************
def index_calc(request):
    return render(request, 'mathematic/index_calc.html',)

#*************Ctverec************************************************************
def index_ctverec(request):
    return render(request, 'mathematic/index_ctverec.html',)

def choose_ctverec(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'ac':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_ctverec.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'oc':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_ctverec.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'sc':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_ctverec.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'uc':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_ctverec.html', {'myfield': myfield})

def count_ctverec(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'ac':
            if request.GET['cislo1']:
                cislo1_ = float(request.GET['cislo1'])
                cislo1 = str(cislo1_)
                obvod_ = 4*cislo1_
                obvod = str(obvod_)
                obsah_ = pow(cislo1_, 2)
                obsah = str(obsah_)
                uhlopricka_ = cislo1_*sqrt(2)
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_ctverec.html', {
                    'cislo1': cislo1,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_ctverec.html', {
                    'error_message': error_message,
                    })
        elif request.GET['myfield'] == 'oc':
            if request.GET['cislo2']:
                obvod_ = float(request.GET['cislo2'])
                obvod = str(obvod_)
                cislo2_ = obvod_/4
                cislo2 = str(cislo2_)
                obsah_ = pow(cislo2_, 2)
                obsah = str(obsah_)
                uhlopricka_ = cislo2_*sqrt(2)
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_ctverec.html', {
                    'cislo2': cislo2,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_ctverec.html', {
                    'error_message': error_message,
                    })
        elif request.GET['myfield'] == 'sc':
            if request.GET['cislo3']:
                obsah_ = float(request.GET['cislo3'])
                obsah = str(obsah_)
                cislo3_ = sqrt(obsah_)
                cislo3 = str(cislo3_)
                obvod_ = 4*cislo3_
                obvod = str(obvod_)
                uhlopricka_ = cislo3_*sqrt(2)
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_ctverec.html', {
                    'cislo3': cislo3,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_ctverec.html', {
                    'error_message': error_message,
                    })
        elif request.GET['myfield'] == 'uc':
            if request.GET['cislo4']:
                uhlopricka_ = float(request.GET['cislo4'])
                uhlopricka = str(uhlopricka_)
                cislo4_ = uhlopricka_/sqrt(2)
                cislo4 = str(cislo4_)
                obvod_ = 4*cislo4_
                obvod = str(obvod_)
                obsah_ = pow(cislo4_, 2)
                obsah = str(obsah_)
                return render(request, 'mathematic/index_ctverec.html', {
                    'cislo4': cislo4,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_ctverec.html', {
                    'error_message': error_message,
                    })

#*************Obdelnik************************************************************
def index_obdelnik(request):
    return render(request, 'mathematic/index_obdelnik.html')
def choose_obdelnik(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'abo':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_obdelnik.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'aboo':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_obdelnik.html', {'myfield': myfield})
        elif request.GET['myfield'] == 'abso':
            myfield = request.GET['myfield']
            return render(request, 'mathematic/index_obdelnik.html', {'myfield': myfield})

def count_obdelnik(request):
    if request.method == 'GET':
        if request.GET['myfield'] == 'abo':
            if request.GET['cislo1'] and request.GET['cislo2']:
                cislo1_ = float(request.GET['cislo1'])
                cislo1 = str(cislo1_)
                cislo2_ = float(request.GET['cislo2'])
                cislo2 = str(cislo2_)
                obvod_ = 2*(cislo1_+cislo2_)
                obvod = str(obvod_)
                obsah_ = cislo1_*cislo2_
                obsah = str(obsah_)
                uhlopricka_ = sqrt(pow(cislo1_, 2)+pow(cislo2_, 2))
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_obdelnik.html', {
                    'cislo1': cislo1,
                    'cislo2': cislo2,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    'username': username })
            else:
                error_message = 'Musis zadat cislo'
                username = request.user.username
                return render(request, 'mathematic/index_obdelnik.html', {
                    'error_message': error_message,
                    'username': username,
                    })
        elif request.GET['myfield'] == 'aboo':
            if request.GET['cislo3'] and request.GET['cislo4']:
                cislo3_ = float(request.GET['cislo3'])
                cislo3 = str(cislo3_)
                obvod_ = float(request.GET['cislo4'])
                obvod = str(obvod_)
                cislo4_ = (obvod_/2)-cislo3_
                cislo4 = str(cislo4_)
                obsah_ = cislo3_*cislo4_
                obsah = str(obsah_)
                uhlopricka_ = sqrt(pow(cislo3_, 2)+pow(cislo4_, 2))
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_obdelnik.html', {
                    'cislo3': cislo3,
                    'cislo4': cislo4,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka,
                    })
            else:
                username = request.user.username
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_obdelnik.html', {
                    'error_message': error_message,})
        elif request.GET['myfield'] == 'abso':
            if request.GET['cislo5'] and request.GET['cislo6']:
                cislo5_ = float(request.GET['cislo6'])
                cislo5 = str(cislo5_)
                obsah_ = float(request.GET['cislo5'])
                obsah = str(obsah_)
                cislo6_ = obsah_/cislo5_
                cislo6 = str(cislo6_)
                obvod_ = 2*(cislo5_+cislo6_)
                obvod = str(obvod_)
                uhlopricka_ = sqrt(pow(cislo5_, 2)+pow(cislo6_, 2))
                uhlopricka = str(uhlopricka_)
                return render(request, 'mathematic/index_obdelnik.html', {
                    'cislo5': cislo5,
                    'cislo6': cislo6,
                    'obvod': obvod,
                    'obsah': obsah,
                    'uhlopricka': uhlopricka, })
            else:
                error_message = 'Musis zadat cislo'
                return render(request, 'mathematic/index_obdelnik.html', {
                    'error_message': error_message,
                    'username': username,
                    'full_name': request.user.first_name + ' ' + request.user.last_name})

def schedule(request):
    args = {}
    args['now'] = str(datetime.datetime.now().day)+'.' + str(timezone.now().month)+'.'
    weeks = [
    ['31.8. 2015 -  4.9. 2015', '31.8. 2015 - 4.9. 2015', 'Bi 1', 'Ch 2'],
    ['7 .9. 2015 - 11.9. 2015', '7.9. 2015 - 11.9. 2015', 'Ch 1', 'F 2'],
    ['14.9. 2015 - 18.9. 2015', '14.9. 2015 - 18.9. 2015', 'Ch 1', 'Bi 2'],
    ['21.9. 2015 - 25.9. 2015', '21.9. 2015 - 25.9. 2015', 'F 1', 'Ch 2'],
    ['28.9. 2015 - 2.10. 2015', '28.9. 2015 - 2.10. 2015', 'Bi 1', 'Ch 2'],
    ['5 .10. 2015- 9.10. 2015', '5.10. 2015 - 9.10. 2015', 'Ch 1', 'F 2'],
    ['12.10. 2015-16.10. 2015', '12.10. 2015 - 16.10. 2015', 'Ch 1', 'Bi 2'],
    ['19.10. 2015-23.10. 2015', '19.10. 2015 - 23.10. 2015', 'F 1', 'Ch 2'],
    ['26.10. 2015-30.10. 2015', '26.10. 2015 - 30.10. 2015', 'Bi 1', 'Ch 2'],
    ['2 .11. 2015- 6.11. 2015', '2.11. 2015 - 6.11. 2015', 'Ch 1', 'F 2'],
    ['9 .11. 2015-13.11. 2015', '9.11. 2015 - 13.11. 2015', 'Ch 1', 'Bi 2'],
    ['16.11. 2015-20.11. 2015', '16.11. 2015 - 20.11. 2015', 'F 1', 'Ch 2'],
    ['23.11. 2015-27.11. 2015', '23.11. 2015 - 27.11. 2015', 'Bi 1', 'Ch 2'],
    ['30.11. 2015- 4.12. 2015', '30.11. 2015 - 4.12. 2015', 'Ch 1', 'F 2'],
    ['7 .12. 2015-11.12. 2015', '7.12. 2015 - 11.12. 2015', 'Ch 1', 'Bi 2'],
    ['14.12. 2015-18.12. 2015', '14.12. 2015 - 18.12. 2015', 'F 1', 'Ch 2'],
    ['21.12. 2015-25.12. 2015', '21.12. 2015 - 25.12. 2015', 'Bi 1', 'Ch 2'],
    ['28.12. 2015 - 1.1. 2016', '28.12. 2015 - 1.1. 2016', '__ _', '__ _'],
    ['4 .1. 2016 -  8.1. 2016', '4.1. 2016 - 8.1. 2016', 'Ch 1', 'F 2'],
    ['11.1. 2016 - 15.1. 2016', '11.1. 2016 - 15.1. 2016', 'Ch 1', 'Bi 2'],
    ['18.1. 2016 - 22.1. 2016', '18.1. 2016 - 22.1. 2016', 'F 1', 'Ch 2'],
    ['25.1. 2016 - 29.1. 2016', '25.1. 2016 - 29.1. 2016', 'Bi 1', 'Ch 2'],
    ['1 .2. 2016 -  5.2. 2016', '1.2. 2016 - 5.2. 2016', 'Ch 1', 'F 2'],
    ['8 .2. 2016 - 12.2. 2016', '8.2. 2016 - 12.2. 2016', '__ _', '__ _'],
    ['15.2. 2016 - 19.2. 2016', '15.2. 2016 - 19.2. 2016', 'F 1', 'Ch 2'],
    ['22.2. 2016 - 26.2. 2016', '22.2. 2016 - 26.2. 2016', 'Ch 1', 'F 2'],
    ['29.2. 2016 -  4.3. 2016', '29.2. 2016 - 4.3. 2016', 'F 1', 'Ch 2'],
    ['7 .3. 2016 - 11.3. 2016', '7.3. 2016 - 11.3. 2016', 'Ch 1', 'F 2'],
    ['14.3. 2016 - 18.3. 2016', '14.3. 2016 - 18.3. 2016', 'F 1', 'Ch 2'],
    ['21.3. 2016 - 25.3. 2016', '21.3. 2016 - 25.3. 2016', 'Ch 1', 'F 2'],
    ['28.3. 2016 -  1.4. 2016', '28.3. 2016 - 1.4. 2016', 'F 1', 'Ch 2'],
    ['4 .4. 2016 -  8.4. 2016', '4.4. 2016 - 8.4. 2016', 'Ch 1', 'F 2'],
    ['11.4. 2016 - 15.4. 2016', '11.4. 2016 - 15.4. 2016', 'F 1', 'Ch 2'],
    ['18.4. 2016 - 22.4. 2016', '18.4. 2016 - 22.4. 2016', 'Ch 1', 'F 2'],
    ['25.4. 2016 - 29.4. 2016', '25.4. 2016 - 29.4. 2016', 'Ch 2', 'F 1'],
    ['2 .5. 2016 -  6.5. 2016', '2.5. 2016 - 6.5. 2016', 'Ch 1', 'F 2'],
    ['9 .5. 2016 - 13.5. 2016', '9.5. 2016 - 13.5. 2016', 'F 1', 'Ch 2'],
    ['16.5. 2016 - 20.5. 2016', '16.5. 2016 - 20.5. 2016', 'Ch 1', 'F 2'],
    ['23.5. 2016 - 27.5. 2016', '23.5. 2016 - 27.5. 2016', 'F 1', 'Ch 2'],
    ['30.5. 2016 -  3.6. 2016', '30.5. 2016 - 3.6. 2016', 'Ch 1', 'F 2'],
    ['6 .6. 2016 - 10.6. 2016', '6.6. 2016 - 10.6. 2016', 'F 1', 'Ch 2'],
    ['13.6. 2016 - 17.6. 2016', '13.6. 2016 - 17.6. 2016', 'Ch 1', 'F 2'],
    ['20.6. 2016 - 24.6. 2016', '20.6. 2016 - 24.6. 2016', 'F 1', 'Ch 2'],
    ]
    for week in weeks:
        for item in week[0:1]:
            day = str(item)
            week.append(str(int(day[0:len(day)-21])+1)+day[2:6])
            week.append(str(int(day[0:len(day)-21])+2)+day[2:6])
            week.append(str(int(day[0:len(day)-21])+3)+day[2:6])
            week.append(str(int(day[0:len(day)-21])+4)+day[2:6])
            week.append(str(int(day[0:len(day)-21])+5)+day[2:6])
    args['weeks'] = weeks
    return render(request, 'mathematic/schedule.html', args)
