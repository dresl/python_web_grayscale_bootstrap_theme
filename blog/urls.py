from django.conf.urls import patterns, include, url

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.blogs, name='indexb'),
    url(r'^choose-by-age/$', views.choose_order_blog_by_age, name='choose_order_blog_by_age'),
    url(r'^choose-by-year/$', views.choose_order_blog_by_year, name='choose_order_blog_by_year'),
    url(r'^(?P<blog_id>\d+)/$', views.blog, name='detailb'),
    url(r'^like/(?P<blog_id>\d+)/$', views.like_blog, name='like'),
    url(r'^unlike/(?P<blog_id>\d+)/$', views.unlike_blog, name='unlike'),
    url(r'^create/$', views.create_blog, name='createb'),
    url(r'^search/$', views.search_titles, name='search_titles'),
    url(r'^add-comment/$', views.add_comment, name='add_comment'),
    url(r'^delete-comment/$', views.delete_comment, name='delete_comment')
)
