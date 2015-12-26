from django.conf.urls import patterns, include, url

from userprofile import views

urlpatterns = patterns('',
	url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalid/$', views.invalid_login),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^profile/(?P<user_slug>[\w-]+)-(?P<user_id>\d+)/$', views.userprofile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
)