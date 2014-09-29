from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'realcost.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
