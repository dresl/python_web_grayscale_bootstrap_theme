from django.conf.urls import patterns, include, url
from hello import views

urlpatterns = patterns('',
	url(r'^bla$', views.greetings, name='all'),
    url(r'^(?P<greeting_id>\d+)/$', views.greeting, name='index'),
)