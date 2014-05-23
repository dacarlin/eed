from django.conf.urls import patterns, url

from enter import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
)
