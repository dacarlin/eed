from django.db import models

class Entry(models.Model):
  # defines one entry in the EED 
  pub_date    = models.DateTimeField(auto_now=True)

  SYSTEMS = (('BGL', 'Bagel'), )
  system      = models.CharField(max_length=80, choices=SYSTEMS)
  uniprot_ID  = models.CharField(max_length=6, editable=False)
  pdb_ID      = models.CharField("PDB ID", max_length=4, editable=False)
  ec_number   = models.CharField("EC number", max_length=12, editable=False)

  mutations   = models.CharField(max_length=100)
  substrate   = models.CharField(max_length=100)
 
  yyield      = models.FloatField("Yield (mg/mL)") 
  k_cat       = models.FloatField("k_cat") 
  err_k_cat   = models.FloatField()
  k_M         = models.FloatField()
  err_K_M     = models.FloatField()
  over        = models.FloatField()
  err_over    = models.FloatField()

  lane_image  = models.FileField(upload_to="your/mom", blank=True, null=True)

from django.forms import ModelForm
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

class EntryForm(ModelForm):
  class Meta:
    model = Entry
    fields = '__all__'
    exclude = [ ]

  #def save(self):
   # if not self.auto_id:
    #  self.uniprot_ID = 'uni'
     # self.ec_number = '2.3.2'
     # self.pdb_ID = 'hgg2'
    #super(EntryForm, self).save()

class EntryFormPreview(FormPreview):
  def done(self, request, cleaned_data):
    f = EntryForm(request.POST)
    n = f.save()
    return HttpResponseRedirect('/enter/success')
