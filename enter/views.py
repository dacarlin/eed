from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import Entry, EntryForm

def browse(request):
  entry_list = Entry.objects.order_by('entry_ID')
  return render(request, 'enter/browse.html', {'entry_list': entry_list})

def index(request):
  return render(request, 'enter/index.html')

def help(request):
  return render(request, 'enter/help.html')

def systems(request):
  return render(request, 'enter/systems.html')

def submit(request):
  if request.method == 'POST':
    form = EntryForm(request.POST)
    if form.is_valid():
      instance = EntryForm(request.POST, request.FILES)
      data = instance.save() # add arg commit=False to create but not save
      return HttpResponseRedirect('/confirm/')
  else: 
    form = EntryForm()
  return render(request, 'enter/submit.html', {'form':form,})

def confirm(request):
  return render(request, 'enter/confirm.html')
