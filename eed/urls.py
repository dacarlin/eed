from django.conf.urls import patterns, include, url
from django.contrib import admin
from enter import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eed.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^enter/', include('enter.urls')),
  url(r'^browse/', views.browse, name='browse'),
  url(r'^submit/', views.submit, name='submit'),
  url(r'^help/'  , views.help,   name='help'),
  url(r'^systems/', views.systems, name='systems'),
)



