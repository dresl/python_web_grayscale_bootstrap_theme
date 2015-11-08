from django.conf.urls import patterns, include, url

from mathematic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),  
    url(r'^create/$', views.create, name='createb'),
    url(r'^brigade/$', views.BrigadeIndexView.as_view(), name='brigade_index'),
    url(r'^brigade/(?P<pk>\d+)/$', views.DetailView, name='detailb'),
    url(r'^calc/$', views.CalcIndexView.as_view(), name='calc_index'),
    url(r'^calc/choose$', views.choose, name='choose'),
    url(r'^calc/count/$', views.count, name='count'),
)