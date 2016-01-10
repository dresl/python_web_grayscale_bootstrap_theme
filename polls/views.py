# -*- coding: utf-8 -*-
from blog.models import Blog
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import *
from django.utils import timezone
from django.views import generic
from mathematic.models import Brigade, Day
from polls.models import Choice, Question, Sidebar
from django.template.defaulttags import register

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]

################## OTHER ####################################################


def db(request):
    sidebar = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request,
                      'polls/dbnew.html', {'sidebar': sidebar})


def basehtml(request):
    blogs = Blog.objects.all().order_by('-pub_date')[:3]
    sidebar = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    brigades = Brigade.objects.all().order_by('-pub_date')[:5]
    now = timezone.now()
    return render(request,
                      'includes/base.html', {
                        'now': now,
                        'sidebar': sidebar,
                        'brigades': brigades
                      })


def HelloworldView(request):
    sidebar = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'polls/helloworld.html', {'sidebar': sidebar})


def WelcomeView(request):
    sidebar = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')
    blogs = Blog.objects.all().order_by('-pub_date')[:3]
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        brigades = Brigade.objects.filter(pub_date__lte=timezone.now(), owner=user)
    else:
        users = User.objects.all()
        brigades = Brigade.objects.exclude(pub_date__lte=timezone.now(), owner=users)
    return render(request, 'polls/welcome.html', {
            'sidebar': sidebar,
            'brigades': brigades,
            'blogs': blogs
        })

def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response

############# QUESTIONS AND CHOICES ######################################


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/resultsq.html'

    def get_context_data(self, *args, **kwargs):

        context = super(ResultsView, self).get_context_data(*args, **kwargs)
        return context


class InfoView(generic.DetailView):
    model = Question
    template_name = 'polls/infoq.html'

    def get_context_data(self, *args, **kwargs):

        context = super(InfoView, self).get_context_data(*args, **kwargs)
        return context


class IndexView(generic.ListView):
    template_name = 'polls/indexq.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, *args, **kwargs):

        context = super(IndexView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detailq.html'

    def get_context_data(self, *args, **kwargs):

        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context['colors'] = {
 'AliceBlue':'AliceBlue',
 'AntiqueWhite':'AntiqueWhite',
 'Aqua':'Aqua',
 'Akvamarín':'Aquamarine',
 'Blankyt':'Azure',
 'Béžová':'Beige',
 'Biskvit':'Bisque',
 'Černá':'Black',
 'BlanchedAlmond':'BlanchedAlmond',
 'Modra':'Blue',
 'BlueViolet':'BlueViolet',
 'Hnědá':'Brown',
 'Pískově hnědá':'BurlyWood',
 'CadetBlue':'CadetBlue',
 'Chartreuska':'Chartreuse',
 'Čokoláda':'Chocolate',
 'Korál':'Coral',
 'CornflowerBlue':'CornflowerBlue',
 'Cornsilk':'Cornsilk',
 'Karmínový':'Crimson',
 'Tyrkysová':'Cyan',
 'Tmavě modrá':'DarkBlue', 
 'DarkCyan':'DarkCyan',
 'DarkGoldenRod':'DarkGoldenRod',
 'Tmavě šedá':'DarkGray', 
 'Tmavošedý':'DarkGrey',
 'Tmavozelený':'DarkGreen',
 'DarkKhaki':'DarkKhaki',
 'DARKMagenta':'DarkMagenta',
 'DarkOliveGreen':'DarkOliveGreen',
 'DarkOrange':'DarkOrange',
 'DarkOrchid':'DarkOrchid',
 'Tmavě červená':'DarkRed', 
 'DarkSalmon':'DarkSalmon',
 'DarkSeaGreen':'DarkSeaGreen',
 'DarkSlateBlue':'DarkSlateBlue',
 'DarkSlateGray':'DarkSlateGray',
 'DarkSlateGrey':'DarkSlateGrey',
 'DarkTurquoise':'DarkTurquoise',
 'DarkViolet':'DarkViolet',
 'DeepPink':'DeepPink',
 'DeepSkyBlue':'DeepSkyBlue',
 'DimGray':'DimGray',
 'DimGrey':'DimGrey',
 'DodgerBlue':'DodgerBlue',
 'Cihla':'FireBrick',
 'FloralWhite':'FloralWhite',
 'ForestGreen':'ForestGreen',
 'Fuchsie':'Fuchsia',
 'Gainsboro':'Gainsboro',
 'GhostWhite':'GhostWhite',
 'Zlatá':'Gold',
 'Goldenrod':'GoldenRod',
 'Šedá':'Gray',
 'Šedá':'Grey',
 'Zelená':'Green',
 'GreenYellow':'GreenYellow',
 'Medovice':'HoneyDew',
 'HotPink':'HotPink',
 'IndianRed':'IndianRed', 
 'Indigo':'Indigo', 
 'Slonovinová':'Ivory', 
 'Khaki':'Khaki',
 'Levandule':'Lavender',
 'LavenderBlush':'LavenderBlush',
 'LawnGreen':'LawnGreen',
 'LemonChiffon':'LemonChiffon',
 'Světle modrá':'LightBlue', 
 'LightCoral':'LightCoral',
 'LightCyan':'LightCyan',
 'LightGoldenRodYellow':'LightGoldenRodYellow',
 'Světle šedá':'LightGray', 
 'Světle šedá':'LightGrey', 
 'Světle zelená':'LightGreen', 
 'Světle růžová':'LightPink', 
 'LightSalmon':'LightSalmon',
 'LightSeaGreen':'LightSeaGreen',
 'LightSkyBlue':'LightSkyBlue',
 'LightSlateGray':'LightSlateGray',
 'LightSlateGrey':'LightSlateGrey',
 'LightSteelBlue':'LightSteelBlue',
 'LightYellow':'LightYellow',
 'Vápno':'Lime',
 'Limetkově zelená':'LimeGreen', 
 'Prádlo':'Linen',
 'Magenta':'Magenta',
 'Maroon':'Maroon',
 'Medium AquaMarine':'MediumAquaMarine', 
 'Středně modrá':'MediumBlue', 
 'MediumOrchid':'MediumOrchid',
 'MediumPurple':'MediumPurple',
 'MediumSeaGreen':'MediumSeaGreen',
 'MediumSlateBlue':'MediumSlateBlue',
 'MediumSpringGreen':'MediumSpringGreen',
 'Medium Turquoise':'MediumTurquoise', 
 'MediumVioletRed':'MediumVioletRed',
 'MidnightBlue':'MidnightBlue',
 'MintCream':'MintCream',
 'MistyRose':'MistyRose',
 'Mokasín':'Moccasin',
 'NavajoWhite':'NavajoWhite',
 'Navy':'Navy',
 'OldLace':'OldLace',
 'Olivový':'Olive',
 'OliveDrab':'OliveDrab',
 'Pomerančový':'Orange',
 'OrangeRed':'OrangeRed',
 'Orchidej':'Orchid',
 'PaleGoldenRod':'PaleGoldenRod',
 'PaleGreen':'PaleGreen',
 'PaleTurquoise':'PaleTurquoise',
 'PaleVioletRed':'PaleVioletRed',
 'PapayaWhip':'PapayaWhip',
 'PeachPuff':'PeachPuff',
 'Peru':'Peru',
 'Růžový':'Pink',
 'Švestka':'Plum',
 'PowderBlue':'PowderBlue',
 'Purple':'Purple',
 'RebeccaPurple':'RebeccaPurple',
 'Červený':'Red',
 'RosyBrown':'RosyBrown',
 'Královská modrá':'RoyalBlue', 
 'SaddleBrown':'SaddleBrown',
 'Losos':'Salmon',
 'Sandybrown':'SandyBrown',
 'Seagreen':'SeaGreen',
 'Mušle':'SeaShell',
 'Oranžověžlutá':'Sienna',  
 'Stříbro':'Silver',
 'Modrá obloha':'SkyBlue', 
 'SlateBlue':'SlateBlue',
 'SlateGray':'SlateGray',
 'SlateGrey':'SlateGrey',
 'Sněžení':'Snow',
 'SpringGreen':'SpringGreen',
 'SteelBlue':'SteelBlue',
 'Opálení':'Tan',
 'Teal':'Teal',
 'Bodlák':'Thistle',
 'Rajče':'Tomato',
 'Tyrkysový':'Turquoise',
 'Fialový':'Violet',
 'Pšenice':'Wheat',
 'Bílá':'White',
 'WhiteSmoke':'WhiteSmoke',
 'Žlutá':'Yellow',
 'Žlutozelená':'YellowGreen',
}
        return context

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
            'error_message': "Nevybral jste možnost.",
            'username': request.user.username,
            'full_name': request.user.first_name + ' ' + request.user.last_name
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:resultsq', args=(p.id,)))


######### SIDEBAR VIEW ###################################################

def SidebarView(request):
    sidebar = Sidebar.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')[:50]
    return render(request, 'polls/test.html', {'sidebar': sidebar})


######### SEARCH AJAX ####################################################

def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    greetings = Question.objects.filter(title__contains=search_text)
    return render(request, 'polls/ajax_search.html', {
            'greetings': greetings
        })
