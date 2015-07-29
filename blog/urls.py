from django.conf.urls import patterns, include, url

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.blogs, name='indexb'),
    url(r'^(?P<blog_id>\d+)/$', views.blog, name='detailb'),
    url(r'^like/(?P<blog_id>\d+)/$', views.like_blog, name='like'),
    url(r'^create/$', views.create_blog, name='createb'),
    url(r'^search/$', views.search_titles, name='search_titles'),
)
