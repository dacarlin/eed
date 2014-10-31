from django.shortcuts import render, redirect
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

def success(request):
  entry_list = Entry.objects.all().order_by('-pub_date')
  return render(request, 'enter/browse.html', {'entry_list': entry_list})

def previ(request):
  if request.method == 'GET':
    form = EntryForm()
    return render(request, 'enter/systems.html', {'form': form})
  elif request.method == 'POST':
    form = EntryForm(request.POST)
    if form.is_valid():
      if request.POST.get('commit',False):
        instance = form.save(commit=True)
        return redirect('browse')
      else:
        instance = form.save(commit=False)
        return render(request, 'enter/preview.html', {'form': form, 'instance': instance})
    else:
      return render(request, 'enter/systems.html', {'form': form})
