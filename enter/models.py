from django.db import models
from django.forms import ModelForm, ValidationError
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe # for including HTML in names

def check_password(password):
  if password != 'seek':
    raise ValidationError("Please enter the password to submit")

class Entry(models.Model):
  SYSTEMS = ( ("BglB", "Beta-glucosidase B"), ("MDH", "Mannitol dehydrogenase") )
  system      = models.CharField(max_length=80, choices=SYSTEMS)
  mutations   = models.CharField(max_length=100) 
  # for parsing mutations ([a-zA-Z])(\d+)([a-zA-Z)\+*
  yyield      = models.FloatField("Yield (mg/mL)")
  k_cat       = models.FloatField("k_cat (1/min)")
  err_k_cat   = models.FloatField("Standard error, k_cat")
  K_M         = models.FloatField("K_M (mol/L)")
  err_K_M     = models.FloatField("Standard error, K_M")
  lane_image  = models.FileField(upload_to="uploads", blank=True, null=True)
  submitter   = models.CharField("Name", max_length=100)
  institution = models.CharField("School", max_length=100)
  password    = models.CharField(max_length=12, validators=[check_password])

  pub_date    = models.DateTimeField(auto_now=True)
  uniprot_ID  = models.CharField(max_length=6)
  pdb_ID      = models.CharField(max_length=4)
  ec_number   = models.CharField(max_length=12)
  substrate   = models.CharField(max_length=100)
  cid         = models.CharField(max_length=5)
  over        = models.FloatField()
  err_over    = models.FloatField()
  public      = models.BooleanField(default=False)


  def __str__(self):
    return "Entry " + str(self.id) + " (" + self.system + \
           ") published " + str(self.pub_date)[:11] 

class EntryForm(ModelForm):
  class Meta:
    model = Entry
    fields = '__all__'
    exclude = 'public', 'uniprot_ID', 'pdb_ID', 'ec_number', \
              'pub_date', 'over', 'err_over', 'substrate', 'cid'

  def save(self, commit=True):
    instance = super(EntryForm, self).save(commit=False)

    # BglB 2JIE 3.2.1.21 P22073
    # Fill in excluded values
    if instance.system == 'BglB':
      instance.uniprot_ID = 'P22073'
      instance.pdb_ID = '2JIE'
      instance.ec_number = '3.2.1.21'
      instance.substrate = '4-nitrophenyl-beta-D-glucoside'
      instance.cid = '92930'

    # MDH
    if instance.system == 'MDH':
      instance.uniprot_ID = 'MDH Uniprot'
      instance.pdb_ID = 'MDH PDB'
      instance.ec_number = 'MDH EC'
      instance.substrate = 'MDH substrate'
      instance.cid = 'mdh substrate'

    # Parse mutations 
    # Handle space, comma, and plus-delimited lists of one or more
      
    # Calculate k_cat/K_M and propagate standard error
    instance.over = instance.k_cat / instance.K_M
    instance.err_over = instance.err_k_cat / instance.k_cat + \
                        instance.err_K_M / instance.K_M

    if commit:
      instance.save()
    return instance

class EntryFormPreview(FormPreview):
  preview_template = 'enter/preview.html'
  form_template = 'enter/submit.html'

  def done(self, request, cleaned_data):
    f = EntryForm(request.POST)
    f.save()
    return HttpResponseRedirect('/enter/success')
