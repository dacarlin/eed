from django.conf.urls import patterns, url
from django import forms
from enter.models import EntryForm, EntryFormPreview
from enter import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^browse/', views.browse, name='browse'),
  # url(r'^submit/', views.submit, name='submit'),
  url(r'^submit/', EntryFormPreview(EntryForm)),
  url(r'^help/'  , views.help,   name='help'),
  url(r'^systems/', views.systems, name='systems'),
  url(r'^success/', views.success, name='success'),
)
