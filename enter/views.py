from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import DataEntry, DataEntryForm

def adam(request):
  if request.method == 'POST':
    form = DataEntryForm(request.POST)
    if form.is_valid():
      analyses = form.process()
      return render(request, 'enter/preview.html', { 'analyses': analyses, 'form': form, } )
    else:
      return render(request, 'enter/cookbook.html', { 'form': form, } )
  else:
    form = DataEntryForm()
    return render(request, 'enter/cookbook.html', {'form': form} )

def thanks(request):
  form = DataEntryForm(request.POST)
  print(form.is_valid())
  if form.is_valid():
    form.save()
    return render(request, 'enter/thanks.html', {'':''} )
  else:
    return render(request, 'enter/cookbook.html', {'form': form} ) #empty form

def browse(request):
  #entry_list = DataEntry.objects.all().order_by('-pub_date')
  entry_list = DataEntry.objects.all()
  #entry_lits = Entry.objects.all()
  return render(request, 'enter/browse.html', {'entry_list': entry_list})

def index(request):
  return render(request, 'enter/index.html')

def help(request):
  return render(request, 'enter/help.html')
