from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='indexq'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detailq'),
    url(r'^(?P<pk>\d+)/info/$', views.InfoView.as_view(), name='infoq'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='resultsq'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='voteq'),
)