from django.conf.urls import patterns, include, url

from mathematic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^count/$', views.count, name='count'),   
    url(r'^create/$', views.create, name='createb'),
    url(r'^brigade/$', views.BrigadeIndexView.as_view(), name='brigade_index'),
    url(r'^brigade/(?P<pk>\d+)/$', views.DetailView, name='detailb')
)