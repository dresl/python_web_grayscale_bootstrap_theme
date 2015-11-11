from django.conf.urls import patterns, include, url

from mathematic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),  
    url(r'^brigade/create/$', views.create, name='createb'),
    url(r'^brigade/$', views.BrigadeIndexView.as_view(), name='brigade_index'),
    url(r'^brigade/(?P<pk>\d+)/$', views.DetailView, name='detailb'),
    url(r'^calc/$', views.CalcIndexView.as_view(), name='calc_index'),
    #cirle
    url(r'^calc/circle/$', views.index_circle, name='index_circle'),
    url(r'^calc/circle/choose$', views.choose_circle, name='choose_circle'),
    url(r'^calc/circle/count/$', views.count_circle, name='count_circle'),
)