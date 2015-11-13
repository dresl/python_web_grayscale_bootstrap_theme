
from django.conf.urls import include, patterns, url

from leonardo.site import leonardo_admin

urlpatterns = patterns('',
                       url(r'^', include(leonardo_admin.urls)),
                       url(r'^', include('django.contrib.admindocs.urls')),
                       )
