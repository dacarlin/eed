from django.conf.urls import patterns, url

from enter import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^browse/', views.browse, name='browse'),
  url(r'^submit/', views.submit, name='submit'),
)
