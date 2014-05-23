from django.db import models

class Entry(models.Model):
  # defines one entry in the EED
  
  entry_ID    = models.IntegerField()
  pub_date    = models.DateTimeField()

  system      = models.CharField(max_length=80)
  uniprot_ID  = models.CharField(max_length=6)
  pdb_ID      = models.CharField(max_length=4)
  ec_number   = models.CharField(max_length=12)

  mutations   = models.CharField(max_length=100)
  substrate   = models.CharField(max_length=100)
 
  _yield      = models.FloatField() 
  k_cat       = models.FloatField() 
  err_k_cat   = models.FloatField()
  k_M         = models.FloatField()
  err_K_M     = models.FloatField()
  over        = models.FloatField()
  err_over    = models.FloatField()

  lane_image  = models.FileField(upload_to="your/mom")


