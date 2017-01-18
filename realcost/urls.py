from django.conf.urls import include, url
from django.contrib import admin
from .views import *
from realcost import views as realcost_views

urlpatterns = [
    url(r'^$', realcost_views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
