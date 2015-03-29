from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^browse/', views.browse),
    url(r'^methods/', views.methods),
    url(r'^submit/$', views.submit),
    url(r'^thanks/$', views.thanks),
    url(r'^help/', views.help),
    )
