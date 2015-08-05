from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import *
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Question, Greeting, Sidebar
from blog.models import Blog
from mathematic.models import Brigade, Day
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from django.core.context_processors import csrf
from polls.forms import GreetingForm

################## OTHER ####################################################

def db(request):
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        return render(request,'polls/dbnew.html', {'sidebar': sidebar,
                                                   'username': request.user.username,
                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
    else: 
        return render(request, 'polls/dbnew.html', {'sidebar': sidebar})

def basehtml(request):
    blogs = Blog.objects.all().order_by('-pub_date')[:3]
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    brigades = Brigade.objects.all().order_by('-pub_date')[:5]
    now = timezone.now()
    if request.user.is_authenticated():
        return render(request, 'includes/base.html',{'blogs': blogs,
                                                     'sidebar': sidebar,
                                                     'now': now,
                                                     'username': request.user.username,
                                                     'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'includes/base.html', {'sidebar': sidebar, 'brigades': brigades})

def HelloworldView(request):
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    if request.user.is_authenticated():
        return render(request,'polls/helloworld.html', {'sidebar': sidebar,
                                                        'username': request.user.username,
                                                        'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'polls/helloworld.html', {'sidebar': sidebar})

def WelcomeView(request):
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    blogs = Blog.objects.all().order_by('-pub_date')[:2]
    brigades = Brigade.objects.all().order_by('-pub_date')[:5]
    if request.user.is_authenticated():
        return render(request,'polls/welcome.html', {'sidebar': sidebar,
                                                     'blogs': blogs,
                                                     'brigades': brigades,
                                                     'username': request.user.username,
                                                     'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'polls/welcome.html', {'sidebar': sidebar, 'brigades': brigades, 'blogs': blogs})

#################### GREETINGS VIEW ##########################################

def create(request):
    if request.POST:
        form = GreetingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/greeting/')
    else:
        form = GreetingForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    if request.user.is_authenticated():
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['form'] = args['form']
        return render(request, 'polls/create_greeting.html', args)
    else:
        args['form'] = args['form']
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'polls/create_greeting.html', args)

def greetings(request):
    language = 'cs-cz'
    session_language = 'cs-cz'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']
    if 'lang' in request.session:
        session_language = request.session['lang']

    args={}
    args.update(csrf(request))
    args['language'] = language
    args['session_language'] = session_language
    if request.user.is_authenticated():
        args['greetings'] = Greeting.objects.all().order_by('-pub_date')
        args['questions'] = Question.objects.all()
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['language'] = args['language']
        args['session_language'] = args['session_language']
        return render(request,'polls/indexg.html', args)
    else:
        args['greetings'] = Greeting.objects.all().order_by('-pub_date')
        args['language'] = args['language']
        args['session_language'] = args['session_language']
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'polls/indexg.html', args)
    
    return render(request,'polls/indexg.html', args)

def greeting(request, greeting_id=1):
    language = 'en-gb'
    session_language = 'en-gb'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']
    if 'lang' in request.session:
        session_language = request.session['lang']

    args={}
    args.update(csrf(request))
    args['language'] = language
    args['session_language'] = session_language
    if request.user.is_authenticated():
        args['greetings'] = Greeting.objects.all().order_by('-pub_date')
        args['questions'] = Question.objects.all()
        args['greeting'] = Greeting.objects.get(id=greeting_id)
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        args['username'] = request.user.username
        args['full_name'] = request.user.first_name + ' ' + request.user.last_name
        args['language'] = args['language']
        args['session_language'] = args['session_language']
        return render(request,'polls/detailg.html', args)
    else:
        args['greetings'] = Greeting.objects.all().order_by('-pub_date')
        args['language'] = args['language']
        args['session_language'] = args['session_language']
        args['greeting'] = Greeting.objects.get(id=greeting_id)
        args['greetings'] = Greeting.objects.all().order_by('-pub_date')
        args['sidebar'] = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        return render(request, 'polls/detailg.html', args)

def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response

def like_greeting(request, greeting_id):
    if greeting_id:
        a = Greeting.objects.get(id=greeting_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/greeting/%s' % greeting_id)

############# QUESTIONS AND CHOICES ##############################################

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/resultsq.html'

class InfoView(generic.DetailView):
    model = Question
    template_name = 'polls/infoq.html'

class IndexView(generic.ListView):
    template_name = 'polls/indexq.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['full_name'] = request.user.first_name + ' ' + request.user.last_name
        context['username'] = request.user.username
        return context
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detailq.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detailq.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
            'username': request.user.username,
            'full_name': request.user.first_name + ' ' + request.user.last_name,
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:resultsq', args=(p.id,)))


######### SIDEBAR VIEW ########################################################################

def SidebarView(request):
    sidebar = Sidebar.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]
    if request.user.is_authenticated():
        return render(request, 'polls/test.html', {'sidebar': sidebar, 'username': request.user.username,
                                                   'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        return render(request, 'polls/test.html', {'sidebar': sidebar})


######### SEARCH AJAX ###########################################################################

def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    if request.user.is_authenticated():
        greetings = Greeting.objects.filter(title__contains=search_text)
        return render(request,'polls/ajax_search.html', {'greetings': greetings,'username': request.user.username, 
                                                     'full_name': request.user.first_name + ' ' + request.user.last_name})
    else:
        greetings = Greeting.objects.filter(title__contains=search_text)
        return render(request,'polls/ajax_search.html', {'greetings': greetings})