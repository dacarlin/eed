from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
from enter import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eed.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', lambda r : HttpResponseRedirect('enter/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^enter/', include('enter.urls')),
)
