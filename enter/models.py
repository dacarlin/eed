from django.db import models
from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe # for including HTML in names

class Entry(models.Model):
  SYSTEMS = ( ("BglB", "Beta-glucosidease B"), ("MDH", "Mannitol dehydrogenase") )
  system      = models.CharField(max_length=80, choices=SYSTEMS)
  mutations   = models.CharField(max_length=100) # Break into seperate fields
  yyield      = models.FloatField("Yield (mg/mL)")
  k_cat       = models.FloatField("k_cat")
  err_k_cat   = models.FloatField("Standard error, k_cat")
  K_M         = models.FloatField("K_M")
  err_K_M     = models.FloatField("Standard error, K_M")

  # I'll handle these
  pub_date    = models.DateTimeField(auto_now=True)
  uniprot_ID  = models.CharField(max_length=6)
  pdb_ID      = models.CharField(max_length=4)
  ec_number   = models.CharField(max_length=12)
  substrate   = models.CharField(max_length=100)
  over        = models.FloatField()
  err_over    = models.FloatField()

  lane_image  = models.FileField(upload_to="uploads", blank=True, null=True)

class EntryForm(ModelForm):
  class Meta:
    model = Entry
    fields = '__all__'
    exclude = 'uniprot_ID', 'pdb_ID', 'ec_number', \
              'pub_date', 'over', 'err_over', 'substrate'

  def save(self, commit=True):
    instance = super(EntryForm, self).save(commit=False)

    # BglB 2JIE 3.2.1.21 P22073
    # Fill in excluded values
    if instance.system == 'BglB':
      instance.uniprot_ID = 'P22073'
      instance.pdb_ID = '2JIE'
      instance.ec_number = '3.2.1.21'
      instance.substrate = '4-nitrophenyl-beta-D-glucoside'
    if instance.system == 'MDH':
      instance.uniprot_ID = 'MDH Uniprot'
      instance.pdb_ID = 'MDH PDB'
      instance.ec_number = 'MDH EC'
      instance.substrate = 'MDH substrate'

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
