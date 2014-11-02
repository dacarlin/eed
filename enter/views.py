from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from enter.models import Entry, EntryForm, DataEntryForm

def adam(request):
  # if we're getting input from DataEntryForm in cookbook.html
  if request.method == 'POST':
    
    # create a new instance of DataEntryForm from the POST data ... seems odd
    form = DataEntryForm(request.POST)
    
    if form.is_valid():
      analyses = form.process() #returns { 'sample': {'param1': param1, 'param2': param2, ...  } }
      print(analyses)
      return render(request, 'enter/preview.html', { 'analyses': analyses } )
      
    else:
      # if form isn't valid
      pass
  
  else:
    # GET or other request
    form = DataEntryForm()
    return render(request, 'enter/cookbook.html', {'form': form} ) #empty form

def thanks(request):
  if request.method == 'POST':
    form = NameForm(request.POST)
    if form.is_valid():
      # save form to database
      #process the data in form.cleaned_data as needed
      return render(request, 'enter/preview.html', {'form': form } )
  # if GET or other request 
  else:
    form = NameForm()
    return render(request, 'enter/systems.html', {'form': form} )
    
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
    return render(request, 'enter/systems.html', {'form': form} )
  elif request.method == 'POST':
    # ie, it's the form defined by the ModelForm EntryForm
    form = EntryForm(request.POST)
    if form.is_valid():
      if request.POST.get('commit', False):
        # if the post request attribute 'commit' is false
        # display the table of kinetic constants
        return redirect('browse')
      else:
        instance = form.save(commit=False)
        return render(request, 'enter/preview.html', {'form': form, 'instance': instance, } )
    else:
      return render(request, 'enter/systems.html', {'form': form})