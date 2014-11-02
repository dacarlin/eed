# django stuff
from django.db import models
from django.forms import ModelForm, ValidationError
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe # for including HTML in names

# plotting and processing stuff
import io
import pandas
import numpy
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.pyplot as plt
import base64
    
class Entry(models.Model):

  # user-supplied
  mutant = models.CharField(max_length=100,default="a123b")
  yyield = models.FloatField(default="1")
  csv = models.TextField(default="sample,kobs,S\nwt,3.30E-01,0.075\nwt,1.45E-01,0.01875\nwt,7.56E-02,0.00469\nwt,-3.29E-14,0.00117\nwt,1.32E-01,0.00029\nwt,4.46E-02,0.00007\nwt,-1.31E-02,0.00002\nwt,1.45E-02,0\nwt,4.11E-01,0.075\nwt,1.18E-01,0.01875\nwt,7.07E-02,0.00469\nwt,-1.44E-01,0.00117\nwt,-1.04E-01,0.00029\nwt,-4.55E-02,0.00007\nwt,1.67E-02,0.00002\nwt,2.85E-14,0\nwt,3.90E-01,0.075\nwt,9.40E-02,0.01875\nwt,5.62E-02,0.00469\nwt,2.42E-02,0.00117\nwt,8.72E-03,0.00029\nwt,3.01E-02,0.00007\nwt,-8.13E-03,0.00002\nwt,2.03E-01,0.075\nwt,2.53E-01,0.01875\nwt,1.81E-02,0.00469\nwt,2.41E-02,0.00117\nwt,-8.68E-14,0.00007\nwt,-3.66E-02,0.00002\nwt,9.45E-14,0\nwt,2.94E-01,0.075\nwt,8.98E-02,0.01875\nwt,-4.34E-14,0.00469\nwt,-6.75E-14,0.00117\nwt,4.73E-02,0.00029\nwt,5.28E-02,0.00007\nwt,-1.86E-14,0\nwt,3.26E-01,0.075\nwt,2.07E-01,0.01875\nwt,2.95E-02,0.00469\nwt,2.56E-14,0.00117\nwt,-1.75E-14,0.00029\nwt,3.07E-02,0.00007\nwt,-5.08E-02,0.00002\nwt,4.23E+02,0.075\nwt,5.72E+02,0.01875\nwt,3.04E+02,0.00469\nwt,1.32E+02,0.00117\nwt,3.26E+01,0.00029\nwt,9.87E+00,0.00007\nwt,2.60E+00,0.00002\nwt,2.09E-01,0\nwt,7.59E+02,0.075\nwt,4.92E+02,0.01875\nwt,3.12E+02,0.00469\nwt,1.11E+02,0.00117\nwt,3.59E+01,0.00029\nwt,9.64E+00,0.00007\nwt,2.26E+00,0.00002\nwt,5.36E-14,0\nwt,6.23E+02,0.075\nwt,4.36E+02,0.01875\nwt,2.70E+02,0.00469\nwt,1.16E+02,0.00117\nwt,2.86E+01,0.00029\nwt,7.69E+00,0.00007\nwt,2.01E+00,0.00002\nwt,-1.26E-01,0\nwt,6.13E+02,0.075\nwt,6.84E+02,0.01875\nwt,3.81E+02,0.00469\nwt,1.45E+02,0.00117\nwt,4.95E+01,0.00029\nwt,2.65E+01,0.00007\nwt,2.90E+00,0.00002\nwt,2.07E-01,0\nwt,5.64E+02,0.075\nwt,6.80E+02,0.01875\nwt,4.07E+02,0.00469\nwt,1.39E+02,0.00117\nwt,4.42E+01,0.00029\nwt,1.08E+01,0.00007\nwt,2.76E+00,0.00002\nwt,7.79E-02,0\nwt,6.91E+02,0.075\nwt,5.38E+02,0.01875\nwt,4.08E+02,0.00469\nwt,1.63E+02,0.00117\nwt,4.64E+01,0.00029\nwt,1.44E+01,0.00007\nwt,2.33E+00,0.00002\nwt,2.60E-01,0")

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
  results = models.CharField(max_length=1000)

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

    output = io.StringIO()
    output.write(str(instance.csv))
    output.seek(0)

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


    data = pandas.read_csv(output,header=0)
    instance.data = data

    # fits
    def coef(data):
      def mm(S, kcat, km): return kcat*S/(km+S)
      params, cov = curve_fit( mm, data['S'], data['kobs'], p0=(100,0.005) )
      residuals = mm(data['S'],params[0],params[1]) - data['kobs']
      fres = sum(residuals**2)
      error = [ abs(cov[i][i])**0.5 for i in range(len(params)) ]

      def lm(S, m, b): return m*S+b
      lparams, lcov = curve_fit( lm, data['S'], data['kobs'], p0=(1000,0) )
      lresiduals = lm(data['S'],params[0],params[1]) - data['kobs']
      lfres = sum(lresiduals**2)
      lerror = [ abs(lcov[i][i])**0.5 for i in range(len(lparams)) ]

      if lfres < fres:
        eff = ''
        err3 = ''
        return (eff, err3)

      else:
        kcat, km  = params
        err1, err2 = error
        eff, err3 = (kcat/km, kcat/km*(err1/kcat)**2+(err2/km)**2)
        
    instance.results = data.groupby('sample').apply(coef).values    

    # honestly not sure what this does
    if commit:
        instance.save()

    return instance

def check_password(password):
  if password != 'seek':
    raise ValidationError("Please enter the password to submit")

class DataEntry(models.Model):
  csv = models.TextField(default="sample,kobs,S\nwt,3.30E-01,0.075\nwt,1.45E-01,0.01875\nwt,7.56E-02,0.00469\nwt,-3.29E-14,0.00117\nwt,1.32E-01,0.00029\nwt,4.46E-02,0.00007\nwt,-1.31E-02,0.00002\nwt,1.45E-02,0\nwt,4.11E-01,0.075\nwt,1.18E-01,0.01875\nwt,7.07E-02,0.00469\nwt,-1.44E-01,0.00117\nwt,-1.04E-01,0.00029\nwt,-4.55E-02,0.00007\nwt,1.67E-02,0.00002\nwt,2.85E-14,0\nwt,3.90E-01,0.075\nwt,9.40E-02,0.01875\nwt,5.62E-02,0.00469\nwt,2.42E-02,0.00117\nwt,8.72E-03,0.00029\nwt,3.01E-02,0.00007\nwt,-8.13E-03,0.00002\nwt,2.03E-01,0.075\nwt,2.53E-01,0.01875\nwt,1.81E-02,0.00469\nwt,2.41E-02,0.00117\nwt,-8.68E-14,0.00007\nwt,-3.66E-02,0.00002\nwt,9.45E-14,0\nwt,2.94E-01,0.075\nwt,8.98E-02,0.01875\nwt,-4.34E-14,0.00469\nwt,-6.75E-14,0.00117\nwt,4.73E-02,0.00029\nwt,5.28E-02,0.00007\nwt,-1.86E-14,0\nwt,3.26E-01,0.075\nwt,2.07E-01,0.01875\nwt,2.95E-02,0.00469\nwt,2.56E-14,0.00117\nwt,-1.75E-14,0.00029\nwt,3.07E-02,0.00007\nwt,-5.08E-02,0.00002\nwt,4.23E+02,0.075\nwt,5.72E+02,0.01875\nwt,3.04E+02,0.00469\nwt,1.32E+02,0.00117\nwt,3.26E+01,0.00029\nwt,9.87E+00,0.00007\nwt,2.60E+00,0.00002\nwt,2.09E-01,0\nwt,7.59E+02,0.075\nwt,4.92E+02,0.01875\nwt,3.12E+02,0.00469\nwt,1.11E+02,0.00117\nwt,3.59E+01,0.00029\nwt,9.64E+00,0.00007\nwt,2.26E+00,0.00002\nwt,5.36E-14,0\nwt,6.23E+02,0.075\nwt,4.36E+02,0.01875\nwt,2.70E+02,0.00469\nwt,1.16E+02,0.00117\nwt,2.86E+01,0.00029\nwt,7.69E+00,0.00007\nwt,2.01E+00,0.00002\nwt,-1.26E-01,0\nwt,6.13E+02,0.075\nwt,6.84E+02,0.01875\nwt,3.81E+02,0.00469\nwt,1.45E+02,0.00117\nwt,4.95E+01,0.00029\nwt,2.65E+01,0.00007\nwt,2.90E+00,0.00002\nwt,2.07E-01,0\nwt,5.64E+02,0.075\nwt,6.80E+02,0.01875\nwt,4.07E+02,0.00469\nwt,1.39E+02,0.00117\nwt,4.42E+01,0.00029\nwt,1.08E+01,0.00007\nwt,2.76E+00,0.00002\nwt,7.79E-02,0\nwt,6.91E+02,0.075\nwt,5.38E+02,0.01875\nwt,4.08E+02,0.00469\nwt,1.63E+02,0.00117\nwt,4.64E+01,0.00029\nwt,1.44E+01,0.00007\nwt,2.33E+00,0.00002\nwt,2.60E-01,0")
    
class DataEntryForm(ModelForm):
  class Meta:
     model = DataEntry
  
  def process(self):    
    def fit(data):
      sample = data['sample']
      
      def mm(S, kcat, km): return kcat*S/(km+S)
      params, cov = curve_fit( mm, data['S'], data['kobs'], p0=(100,0.005) )
      residuals = mm(data['S'],params[0],params[1]) - data['kobs']
      fres = sum(residuals**2)
      error = [ abs(cov[i][i])**0.5 for i in range(len(params)) ]

      def lm(S, m, b): return m*S+b
      lparams, lcov = curve_fit( lm, data['S'], data['kobs'], p0=(1000,0) )
      lresiduals = lm(data['S'],params[0],params[1]) - data['kobs']
      lfres = sum(lresiduals**2)
      lerror = [ abs(lcov[i][i])**0.5 for i in range(len(lparams)) ]

      if lfres < fres:
        kcat, err1, km, err2 = ['NA' * 4]
        eff, err3 = '', ''

      else:
        kcat, km  = params
        err1, err2 = error
        eff, err3 = (kcat/km, kcat/km*(err1/kcat)**2+(err2/km)**2)
        xdata = numpy.linspace(0,max(data['S']))
        ydata = [  mm(x,params[0],params[1]) for x in xdata ]
        
        stream = io.BytesIO()    
        plt.figure()
        plt.plot(xdata,ydata) 
        plt.savefig(stream, format='png')
        stream.seek(0)
        linear_plot = base64.b64encode(stream.read())
        mm_plot = base64.b64encode(stream.read())
      
      return { 'kcat': kcat, 'err1': err1, 'km': km, 'err2': err2, 'eff': eff, 'err3': err3, 
        'linear_plot': linear_plot, 'mm_plot': mm_plot }
      
    data = pandas.read_csv(io.StringIO(self.cleaned_data['csv']))
    return data.groupby(by='sample').apply(fit).to_dict()