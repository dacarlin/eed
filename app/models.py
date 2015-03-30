import io
import base64
from numpy import linspace
from pandas import read_csv
from django.db.models import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from django.forms import ModelForm, ValidationError

def mm(S, kcat, km): 
  return kcat*S/(km+S)

class Entry(Model):
  # meta
  date = DateTimeField(auto_now_add=True)
  public = BooleanField(default=False)
  
  # bio
  sys = CharField(max_length=10)
  mutant = CharField(max_length=199)
  yyield = FloatField()
  substrate = CharField(max_length=199)
  cid = CharField(max_length=20)
  
  # const
  eff, err3 = FloatField(), FloatField()
  kcat, err1 = FloatField(), FloatField()
  km, err2 = FloatField(), FloatField()
  
  # file-like 
  lin, mm = TextField(), TextField()
  pdb = TextField()
  raw = TextField()

def fit(data):
  
  params, cov = curve_fit( mm, data['s'], data['kobs'], p0=(100,0.005) )
  residuals = mm(data['s'],params[0],params[1]) - data['kobs']
  fres = sum(residuals**2)
  error = [ abs(cov[i][i])**0.5 for i in range(len(params)) ]

  def lm(S, m, b): return m*S+b
  lparams, lcov = curve_fit( lm, data['s'], data['kobs'], p0=(1000,0) )
  lresiduals = lm(data['s'],params[0],params[1]) - data['kobs']
  lfres = sum(lresiduals**2)
  lerror = [ abs(lcov[i][i])**0.5 for i in range(len(lparams)) ]
  
  if lfres < fres:
    kcat, err1, km, err2 = ['NA' * 4]
    eff, err3 = '', ''
    xdata = linspace(0,max(data['s']))
    ydata = [  lm(x,params[0],params[1]) for x in xdata ]

  else:
    kcat, km  = params
    err1, err2 = error
    eff, err3 = (kcat/km, kcat/km*(err1/kcat)**2+(err2/km)**2)
    xdata = linspace(0,max(data['s']))
    ydata = [  mm(x,params[0],params[1]) for x in xdata ]

  stream = io.BytesIO()
  plt.figure()
  plt.grid(True)
  plt.xlabel('Substrate concentration (M)')
  plt.ylabel('Rate observed (M/s)')
  plt.plot(xdata,ydata)
  plt.scatter(data['s'], data['kobs'])
  plt.savefig(stream, format='png')
  stream.seek(0)
  linear_plot = base64.b64encode(stream.read())
  stream.seek(0)
  mm_plot = base64.b64encode(stream.read())

  return {  'substrate': '4-nitrophenyl-beta-D-glucoside',
            'cid' : '92930',
            'yyield': 1.02,
            'kcat': kcat, 'err1': err1, 
            'km': km, 'err2': err2, 
            'eff': eff, 'err3': err3,
            'linear_plot': linear_plot, 'mm_plot': mm_plot }

class DataEntry(Model):
  example = """sample,yield,kobs,s
r240a,1.108,5.13e+03,0.01875
r240a,1.108,2.34e+03,0.00469
r240a,1.108,7.89e+02,0.00117
r240a,1.108,2.30e+02,0.00029
r240a,1.108,6.22e+01,0.00007
r240a,1.108,1.60e+01,0.00002
r240a,1.108,0.00e+00,0.00000
r240a,1.108,8.79e+03,0.07500
r240a,1.108,5.08e+03,0.01875
r240a,1.108,2.44e+03,0.00469
r240a,1.108,7.90e+02,0.00117
r240a,1.108,2.45e+02,0.00029
r240a,1.108,5.89e+01,0.00007
r240a,1.108,1.76e+01,0.00002
r240a,1.108,-1.59e-13,0.00000
r240a,1.108,8.96e+03,0.07500
r240a,1.108,5.16e+03,0.01875
r240a,1.108,2.50e+03,0.00469
r240a,1.108,8.06e+02,0.00117
r240a,1.108,2.18e+02,0.00029
r240a,1.108,5.48e+01,0.00007
r240a,1.108,1.64e+01,0.00002
r240a,1.108,0.00e+00,0.00000
e222a,0.29,7.00e+01,0.07500
e222a,0.29,9.20e+01,0.01875
e222a,0.29,9.93e+01,0.00469
e222a,0.29,5.19e+01,0.00117
e222a,0.29,2.48e+01,0.00029
e222a,0.29,6.84e+00,0.00007
e222a,0.29,2.44e+00,0.00002
e222a,0.29,0.00e+00,0.00000
e222a,0.29,7.08e+01,0.07500
e222a,0.29,8.97e+01,0.01875
e222a,0.29,9.93e+01,0.00469
e222a,0.29,5.53e+01,0.00117
e222a,0.29,2.41e+01,0.00029
e222a,0.29,1.19e+01,0.00007
e222a,0.29,2.43e+00,0.00002
e222a,0.29,1.37e-13,0.00000
e222a,0.29,7.15e+01,0.07500
e222a,0.29,9.24e+01,0.01875
e222a,0.29,1.03e+02,0.00469
e222a,0.29,5.36e+01,0.00117
e222a,0.29,2.25e+01,0.00029
e222a,0.29,6.76e+00,0.00007
e222a,0.29,2.44e+00,0.00002
e222a,0.29,1.26e-13,0.00000
e353a,0.56,1.69e-01,0.07500
e353a,0.56,2.31e-02,0.01875
e353a,0.56,2.06e-02,0.00469
e353a,0.56,5.23e-03,0.00117
e353a,0.56,4.10e-03,0.00029
e353a,0.56,6.26e-03,0.00007
e353a,0.56,8.33e-03,0.00002
e353a,0.56,4.32e-02,0.00000
e353a,0.56,1.83e-01,0.07500
e353a,0.56,4.13e-02,0.01875
e353a,0.56,1.96e-02,0.00469
e353a,0.56,6.09e-03,0.00117
e353a,0.56,5.91e-03,0.00029
e353a,0.56,8.22e-03,0.00007
e353a,0.56,4.58e-03,0.00002
e353a,0.56,1.96e-14,0.00000
e353a,0.56,1.16e-01,0.07500
e353a,0.56,4.12e-02,0.01875
e353a,0.56,1.44e-02,0.00469
e353a,0.56,1.08e-02,0.00117
e353a,0.56,4.67e-03,0.00029
e353a,0.56,2.83e-03,0.00007
e353a,0.56,1.25e-02,0.00002
e353a,0.56,-8.94e-15,0.00000
wt4,1.977,844.140632,0.07500
wt4,1.977,645.227622,0.01875
wt4,1.977,426.722947,0.00469
wt4,1.977,154.396036,0.00117
wt4,1.977,44.925519,0.00029
wt4,1.977,12.195816,0.00007
wt4,1.977,2.918324,0.00002
wt4,1.977,-0.000000,0.00000
wt4,1.977,856.086267,0.07500
wt4,1.977,633.840600,0.01875
wt4,1.977,385.046495,0.00469
wt4,1.977,151.299831,0.00117
wt4,1.977,39.319557,0.00029
wt4,1.977,10.347544,0.00007
wt4,1.977,2.479186,0.00002
wt4,1.977,0.069484,0.00000
wt4,1.977,886.901021,0.07500
wt4,1.977,687.584999,0.01875
wt4,1.977,405.088435,0.00469
wt4,1.977,155.127007,0.00117
wt4,1.977,25.016988,0.00029
wt4,1.977,11.342554,0.00007
wt4,1.977,2.926662,0.00002
wt4,1.977,0.088939,0.00000
"""
  
  csv = TextField(default=example)

class DataEntryForm(ModelForm):
  class Meta:
     model = DataEntry

  def process(self):
    data = read_csv(io.StringIO(self.cleaned_data['csv']))
    # should definitely try to clean up data here, check for S versus s, etc.
    return data.groupby(by='sample').apply(fit).to_dict()
    