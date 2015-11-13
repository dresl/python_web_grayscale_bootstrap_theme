
from django.conf.urls import include, patterns, url

from leonardo.site import leonardo_admin

urlpatterns = patterns('',
                       url(r'^doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(leonardo_admin.urls)),
                       )
