from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from app.models import DataEntry, DataEntryForm, Entry

def adam(request):
  if request.method == 'POST':
    form = DataEntryForm(request.POST)
    if form.is_valid():
      analyses = form.process()
      return render(request, 'app/preview.html', { 'analyses': analyses, 'form': form, } )
    else:
      return render(request, 'app/cookbook.html', { 'form': form, } )
  else:
    form = DataEntryForm()
    return render(request, 'app/cookbook.html', {'form': form} )

def thanks(request):
  if request.method == 'POST':
    form = DataEntryForm(request.POST)
    if form.is_valid():
      analyses = form.process()
      
      for sample in analyses.keys():
        entry = Entry()
        entry.sys = 'BglB'
        entry.mutant = sample
        entry._yield = 1
        entry.substrate = '4-nitro'
        entry.cid = '92930'
        entry.__dict__.update(analyses[sample])
        entry.save()
      
      return render(request, 'app/thanks.html', { 'analyses': analyses, 'form': form, } )
    
    else:
      return render(request, 'app/error.html', { 'form': form, } )
  
  else:
    return redirect(index)

def browse(request):
  entry_list = Entry.objects.all()
  return render(request, 'app/browse.html', {'entry_list': entry_list })

def index(request):
  return render(request, 'app/index.html')

def help(request):
  return render(request, 'app/help.html')
