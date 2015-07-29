from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.greetings, name='indexg'),
    url(r'^(?P<greeting_id>\d+)/$', views.greeting, name='detailg'),
    url(r'^language/(?P<language>[a-z/-]+)/$', views.language, name='language'),
    url(r'^like/(?P<greeting_id>\d+)/$', views.like_greeting, name='like'),
    url(r'^create/$', views.create, name='createg'),
    url(r'^search/$', views.search_titles, name='search_titles'),
)