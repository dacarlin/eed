# django stuff
from django.db import models
from django.forms import ModelForm, ValidationError
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

# plotting and processing stuff
import io
from pandas import read_csv
from numpy import linspace
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.pyplot as plt
import base64

class Entry(models.Model):
  pass

class DataEntry(models.Model):
  csv = models.TextField(default="sample,kobs,S\nwt,3.30E-01,0.075\nwt,1.45E-01,0.01875\nwt,7.56E-02,0.00469\nwt,-3.29E-14,0.00117\nwt,1.32E-01,0.00029\nwt,4.46E-02,0.00007\nwt,-1.31E-02,0.00002\nwt,1.45E-02,0\nwt,4.11E-01,0.075\nwt,1.18E-01,0.01875\nwt,7.07E-02,0.00469\nwt,-1.44E-01,0.00117\nwt,-1.04E-01,0.00029\nwt,-4.55E-02,0.00007\nwt,1.67E-02,0.00002\nwt,2.85E-14,0\nwt,3.90E-01,0.075\nwt,9.40E-02,0.01875\nwt,5.62E-02,0.00469\nwt,2.42E-02,0.00117\nwt,8.72E-03,0.00029\nwt,3.01E-02,0.00007\nwt,-8.13E-03,0.00002\nwt,2.03E-01,0.075\nwt,2.53E-01,0.01875\nwt,1.81E-02,0.00469\nwt,2.41E-02,0.00117\nwt,-8.68E-14,0.00007\nwt,-3.66E-02,0.00002\nwt,9.45E-14,0\nwt,2.94E-01,0.075\nwt,8.98E-02,0.01875\nwt,-4.34E-14,0.00469\nwt,-6.75E-14,0.00117\nwt,4.73E-02,0.00029\nwt,5.28E-02,0.00007\nwt,-1.86E-14,0\nwt,3.26E-01,0.075\nwt,2.07E-01,0.01875\nwt,2.95E-02,0.00469\nwt,2.56E-14,0.00117\nwt,-1.75E-14,0.00029\nwt,3.07E-02,0.00007\nwt,-5.08E-02,0.00002\nwt,4.23E+02,0.075\nwt,5.72E+02,0.01875\nwt,3.04E+02,0.00469\nwt,1.32E+02,0.00117\nwt,3.26E+01,0.00029\nwt,9.87E+00,0.00007\nwt,2.60E+00,0.00002\nwt,2.09E-01,0\nwt,7.59E+02,0.075\nwt,4.92E+02,0.01875\nwt,3.12E+02,0.00469\nwt,1.11E+02,0.00117\nwt,3.59E+01,0.00029\nwt,9.64E+00,0.00007\nwt,2.26E+00,0.00002\nwt,5.36E-14,0\nwt,6.23E+02,0.075\nwt,4.36E+02,0.01875\nwt,2.70E+02,0.00469\nwt,1.16E+02,0.00117\nwt,2.86E+01,0.00029\nwt,7.69E+00,0.00007\nwt,2.01E+00,0.00002\nwt,-1.26E-01,0\nwt,6.13E+02,0.075\nwt,6.84E+02,0.01875\nwt,3.81E+02,0.00469\nwt,1.45E+02,0.00117\nwt,4.95E+01,0.00029\nwt,2.65E+01,0.00007\nwt,2.90E+00,0.00002\nwt,2.07E-01,0\nwt,5.64E+02,0.075\nwt,6.80E+02,0.01875\nwt,4.07E+02,0.00469\nwt,1.39E+02,0.00117\nwt,4.42E+01,0.00029\nwt,1.08E+01,0.00007\nwt,2.76E+00,0.00002\nwt,7.79E-02,0\nwt,6.91E+02,0.075\nwt,5.38E+02,0.01875\nwt,4.08E+02,0.00469\nwt,1.63E+02,0.00117\nwt,4.64E+01,0.00029\nwt,1.44E+01,0.00007\nwt,2.33E+00,0.00002\nwt,2.60E-01,0\na123b,3.30E-01,0.075\na123b,1.45E-01,0.01875\na123b,7.56E-02,0.00469\na123b,-3.29E-14,0.00117\na123b,1.32E-01,0.00029\na123b,4.46E-02,0.00007\na123b,-1.31E-02,0.00002\na123b,1.45E-02,0\na123b,4.11E-01,0.075\na123b,1.18E-01,0.01875\na123b,7.07E-02,0.00469\na123b,-1.44E-01,0.00117\na123b,-1.04E-01,0.00029\na123b,-4.55E-02,0.00007\na123b,1.67E-02,0.00002\na123b,2.85E-14,0\na123b,3.90E-01,0.075\na123b,9.40E-02,0.01875\na123b,5.62E-02,0.00469\na123b,2.42E-02,0.00117\na123b,8.72E-03,0.00029\na123b,3.01E-02,0.00007\na123b,-8.13E-03,0.00002\na123b,2.03E-01,0.075\na123b,2.53E-01,0.01875\na123b,1.81E-02,0.00469\na123b,2.41E-02,0.00117\na123b,-8.68E-14,0.00007\na123b,-3.66E-02,0.00002\na123b,9.45E-14,0\na123b,2.94E-01,0.075\na123b,8.98E-02,0.01875\na123b,-4.34E-14,0.00469\na123b,-6.75E-14,0.00117\na123b,4.73E-02,0.00029\na123b,5.28E-02,0.00007\na123b,-1.86E-14,0\na123b,3.26E-01,0.075\na123b,2.07E-01,0.01875\na123b,2.95E-02,0.00469\na123b,2.56E-14,0.00117\na123b,-1.75E-14,0.00029\na123b,3.07E-02,0.00007\na123b,-5.08E-02,0.00002\na123b,4.23E+02,0.075\na123b,5.72E+02,0.01875\na123b,3.04E+02,0.00469\na123b,1.32E+02,0.00117\na123b,3.26E+01,0.00029\na123b,9.87E+00,0.00007\na123b,2.60E+00,0.00002\na123b,2.09E-01,0\na123b,7.59E+02,0.075\na123b,4.92E+02,0.01875\na123b,3.12E+02,0.00469\na123b,1.11E+02,0.00117\na123b,3.59E+01,0.00029\na123b,9.64E+00,0.00007\na123b,2.26E+00,0.00002\na123b,5.36E-14,0\na123b,6.23E+02,0.075\na123b,4.36E+02,0.01875\na123b,2.70E+02,0.00469\na123b,1.16E+02,0.00117\na123b,2.86E+01,0.00029\na123b,7.69E+00,0.00007\na123b,2.01E+00,0.00002\na123b,-1.26E-01,0\na123b,6.13E+02,0.075\na123b,6.84E+02,0.01875\na123b,3.81E+02,0.00469\na123b,1.45E+02,0.00117\na123b,4.95E+01,0.00029\na123b,2.65E+01,0.00007\na123b,2.90E+00,0.00002\na123b,2.07E-01,0\na123b,5.64E+02,0.075\na123b,6.80E+02,0.01875\na123b,4.07E+02,0.00469\na123b,1.39E+02,0.00117\na123b,4.42E+01,0.00029\na123b,1.08E+01,0.00007\na123b,2.76E+00,0.00002\na123b,7.79E-02,0\na123b,6.91E+02,0.075\na123b,5.38E+02,0.01875\na123b,4.08E+02,0.00469\na123b,1.63E+02,0.00117\na123b,4.64E+01,0.00029\na123b,1.44E+01,0.00007\na123b,2.33E+00,0.00002\na123b,2.60E-01,0")

class DataEntryForm(ModelForm):
  class Meta:
     model = DataEntry

  def process(self):
    def fit(data):
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
        xdata = linspace(0,max(data['S']))
        ydata = [  lm(x,params[0],params[1]) for x in xdata ]

      else:
        kcat, km  = params
        err1, err2 = error
        eff, err3 = (kcat/km, kcat/km*(err1/kcat)**2+(err2/km)**2)
        xdata = linspace(0,max(data['S']))
        ydata = [  mm(x,params[0],params[1]) for x in xdata ]

      stream = io.BytesIO()
      plt.figure()
      plt.grid(True)
      plt.xlabel('Substrate concentration (M)')
      plt.ylabel('Rate observed (M/s)')
      plt.title('Michaels-Menten plot')
      plt.plot(xdata,ydata)
      plt.scatter(data['S'], data['kobs'])
      plt.savefig(stream, format='png')
      stream.seek(0)
      linear_plot = base64.b64encode(stream.read())
      mm_plot = base64.b64encode(stream.read())

      return { 'kcat': kcat, 'err1': err1, 'km': km, 'err2': err2, 'eff': eff, 'err3': err3,
        'linear_plot': linear_plot, 'mm_plot': mm_plot }

    data = read_csv(io.StringIO(self.cleaned_data['csv']))
    return data.groupby(by='sample').apply(fit).to_dict()