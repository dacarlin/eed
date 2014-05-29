from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import Entry, EntryForm

def browse(request):
  entry_list = Entry.objects.filter(public=True)
  return render(request, 'enter/browse.html', {'entry_list': entry_list})

def index(request):
  return render(request, 'enter/index.html')

def help(request):
  return render(request, 'enter/help.html')

def systems(request):
  return render(request, 'enter/systems.html')

def submit(request):
  return render(request, 'enter/submit.html')

def success(request):
  entry_list = Entry.objects.all().order_by('-pub_date')
  return render(request, 'enter/browse.html', {'entry_list': entry_list})
