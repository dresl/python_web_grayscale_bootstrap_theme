from django.conf.urls import patterns, include, url

from mathematic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^brigade/choose-brigade/$', views.choose_brigade, name='choose_brigade'),
    url(r'^brigade/index-create_day/$', views.index_create_day, name='index_create_day'),
    url(r'^brigade/create-day/$', views.create_day, name='create_day'),
    url(r'^brigade/index-create_brigade$', views.index_create_brigade, name='index_create_brigade'),
    url(r'^brigade/create-brigade/$', views.create_brigade, name='create_brigade'),
    url(r'^brigade/$', views.brigade_index_view, name='brigade_index'),
    url(r'^brigade/(?P<brigade_id>\d+)/$', views.brigade_detail_view, name='detailb'),
    #calc
    url(r'^calc/$', views.CalcIndexView.as_view(), name='calc_index'),
    url(r'^calc/calc/$', views.index_calc, name='index_calc'),
    #cirle
    url(r'^calc/circle/$', views.index_circle, name='index_circle'),
    url(r'^calc/circle/choose/$', views.choose_circle, name='choose_circle'),
    url(r'^calc/circle/count/$', views.count_circle, name='count_circle'),
    #ctverec
    url(r'^calc/ctverec/$', views.index_ctverec, name='index_ctverec'),
    url(r'^calc/ctverec/choose/$', views.choose_ctverec, name='choose_ctverec'),
    url(r'^calc/ctverec/count/$', views.count_ctverec, name='count_ctverec'),
    #obdelnik
    url(r'^calc/obdelnik/$', views.index_obdelnik, name='index_obdelnik'),
    url(r'^calc/obdelnik/choose/$', views.choose_obdelnik, name='choose_obdelnik'),
    url(r'^calc/obdelnik/count/$', views.count_obdelnik, name='count_obdelnik'),
    #schedule
    url(r'^rozpis-laborky/$', views.schedule, name='schedule'),
)