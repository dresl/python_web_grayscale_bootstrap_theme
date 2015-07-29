from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import polls.views
import mathematic.views
import gettingstarted.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', polls.views.WelcomeView, name='welcome'),
    url(r'^helloworld/$', polls.views.HelloworldView, name='hello'),
    url(r'^base/$', polls.views.basehtml, name='basehtml'),
    url(r'^db/$', polls.views.db, name='db'),
    url(r'^test/$', polls.views.SidebarView, name='test'),
    url(r'^time/plus/(\d{1,50})/$', gettingstarted.views.hours_ahead, name='time'),
    url(r'^search-form/$', gettingstarted.views.search_form, name='search_form'),
    url(r'^search/$', gettingstarted.views.search, name='search'),
    url(r'^contact/$', gettingstarted.views.contact, name='contact'),
    url(r'^send_email/$', gettingstarted.views.send_email, name='send_email'),
    url(r'^contact/thanks/$', gettingstarted.views.contact_thanks, name='contact_thanks'),
    url(r'^home/$', gettingstarted.views.home, name='home'),
    url(r'^accounts/', include('userprofile.urls', namespace='userprofile')),
    url(r'^math/', include('mathematic.urls', namespace='math')),
    url(r'^polls/', include('polls.urlsq', namespace='polls')),
    url(r'^greeting/', include('polls.urlsg', namespace='greeting')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
)