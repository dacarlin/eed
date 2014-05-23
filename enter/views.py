from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import Entry

def index(request):
  entry_list = Entry.objects.order_by('-entry_ID')
  return render(request, 'enter/index.html', {'entry_list': entry_list})
