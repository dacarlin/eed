import pandas
from django.db import models
from django.forms import ModelForm, ValidationError
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe # for including HTML in names

class Entry(models.Model):

  # instance variables

  # user-supplied
  mutant = models.CharField(max_length=100)
  yyield = models.FloatField("Yield (mg/mL)")
  csv = models.TextField()

  # seek-supplied
  SYSTEMS = ( ("BglB", "Beta-glucosidase B"), ) #only one for now
  system = models.CharField(max_length=80, choices=SYSTEMS) #only one for now
  pub_date = models.DateTimeField(auto_now=True)
  uniprot_ID = models.CharField(max_length=6)
  pdb_ID = models.CharField(max_length=4)
  ec_number = models.CharField(max_length=12)
  substrate = models.CharField(max_length=100) #only one for now
  cid = models.CharField(max_length=5)

  # we'll calculate these
  kcat = models.FloatField()
  err1 = models.FloatField()
  km = models.FloatField()
  err2 = models.FloatField()
  eff = models.FloatField()
  err3 = models.FloatField()

  # display flag
  public = models.BooleanField(default=True)

  def __str__(self):
    return str(self.mutations) + " (" + self.system + \
           ") published " + str(self.pub_date)[:11]

class EntryForm(ModelForm):
  class Meta:
    model = Entry
    fields = 'mutant', 'yyield', 'csv'

  def save(self, commit=True):
    instance = super(EntryForm, self).save(commit=False)

    # for testing
    instance.system = 'BglB'
    instance.kcat = 100
    instance.err1 = 10
    instance.km = 0.001
    instance.err2 = 0.0001
    instance.eff = 1000000000
    instance.err3 = 10

    # BglB 2JIE 3.2.1.21 P22073
    # Fill in excluded values
    if instance.system == 'BglB':
      instance.uniprot_ID = 'P22073'
      instance.pdb_ID = '2JIE'
      instance.ec_number = '3.2.1.21'
      instance.substrate = '4-nitrophenyl-beta-D-glucoside'
      instance.cid = '92930'

    # MDH 1M2W 1.1.1.67 O08355 oh-zero-eight-three-five-five
    # Substrates: D-mannitol and D-arabitol
    if instance.system == 'MDH':
      instance.uniprot_ID = 'MDH Uniprot'
      instance.pdb_ID = 'MDH PDB'
      instance.ec_number = 'MDH EC'
      instance.substrate = 'MDH substrate'
      instance.cid = 'mdh substrate'

    # Parse mutations
    # Handle space, comma, and plus-delimited lists of one or more

    # Calculate k_cat/K_M and propagate standard error
    def eff(kcat, err1, km, err2):
        return (kcat/km, kcat/km*(err1/kcat)**2+(err2/km)**2)

    if commit:
        instance.save()

    return instance

def check_password(password):
  if password != 'seek':
    raise ValidationError("Please enter the password to submit")

class EntryFormPreview(FormPreview):
  preview_template = 'enter/preview.html'
  form_template = 'enter/systems.html'

  def done(self, request, cleaned_data):
    f = EntryForm(request.POST)
    f.save()
    return HttpResponseRedirect('/success')
