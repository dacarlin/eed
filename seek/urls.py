from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
from enter import views
from enter.models import EntryForm, EntryFormPreview

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^help/', views.help),
    url(r'^$', views.index),
    url(r'^browse/', views.browse),
    url(r'^submit/', EntryFormPreview(EntryForm)),
    url(r'^systems/', views.systems),
    url(r'^success/', views.success),
)
