from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import Entry

def browse(request):
  entry_list = Entry.objects.order_by('-entry_ID')
  return render(request, 'enter/browse.html', {'entry_list': entry_list})

def index(request):
  return render(request, 'enter/index.html')

def submit(request):
  entry = get_list_or_404(Entry)
  return render(request, 'enter/submit.html', {'entry': entry})
