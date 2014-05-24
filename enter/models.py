from django.db import models

class Entry(models.Model):
  # defines one entry in the EED
  
  entry_ID    = models.IntegerField()
  pub_date    = models.DateTimeField()

  SYSTEMS = (('BGL', 'Bagel'), )
  system      = models.CharField(max_length=80, choices=SYSTEMS)
  uniprot_ID  = models.CharField(max_length=6)
  pdb_ID      = models.CharField("PDB ID", max_length=4)
  ec_number   = models.CharField("EC number", max_length=12)

  mutations   = models.CharField(max_length=100)
  substrate   = models.CharField(max_length=100)
 
  yyield      = models.FloatField("Yield (mg/mL)") 
  k_cat       = models.FloatField("k_cat") 
  err_k_cat   = models.FloatField()
  k_M         = models.FloatField()
  err_K_M     = models.FloatField()
  over        = models.FloatField()
  err_over    = models.FloatField()

  lane_image  = models.FileField(upload_to="your/mom")

from django.forms import ModelForm

class EntryForm(ModelForm):
  class Meta:
    model = Entry
    fields = '__all__'
    exclude = [
        'pub_date', 'entry_ID', 'uniprot_ID', 'ec_number', 'pdb_ID' ]
