"""
Script plots the multi-observational data set mean to demonstrate different
smoothing techniques

Notes
-----
    Author : Zachary Labe
    Date   : 11 May 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import nclcmaps as ncm
import datetime
import statsmodels.api as sm
import scipy.signal as sts
import scipy as sy
import cmocean

### Define directories
directorydata = '/home/zlabe/Documents/Projects/MAPS_2018/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/MAPS_2018/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting global temperature smoothing - %s----\n' % titletime)

### Alott time series
year1 = 1850
year2 = 2017
years = np.arange(year1,year2+1,1)
months = np.arange(years.shape[0]*12)

### Read in mean observational global surface temperature data
temp = np.genfromtxt(directorydata + 'annual_mean_globaltemps.txt',
                     unpack=True)
print('Completed: Read data!')

### LOWESS smoothing (Locally Weighted Scatterplot Smoothing)
timearray = np.arange(years.shape[0])
smoothed = sm.nonparametric.lowess(temp,timearray,frac=1/5)

### Spline smoothing
spl = sy.interpolate.UnivariateSpline(timearray,temp,k=3,s=1.7)

### Polynomial smoothing
p = np.poly1d(np.polyfit(timearray,temp,6))

### Gaussian smooth
gau = sy.ndimage.filters.gaussian_filter(temp,sigma=3)

###############################################################################
###############################################################################
###############################################################################    
### Plot figure
matplotlib.rc('savefig', facecolor='black')
matplotlib.rc('axes', edgecolor='darkgrey')
matplotlib.rc('xtick', color='darkgrey')
matplotlib.rc('ytick', color='darkgrey')
matplotlib.rc('axes', labelcolor='darkgrey')
matplotlib.rc('axes', facecolor='black')
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']})

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([])
        
fig = plt.figure()
ax = plt.subplot(111) 

adjust_spines(ax, ['left', 'bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_linewidth(0)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=5.5,width=2,which='major',direction='out')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)

plt.plot(years,temp,color='w',linewidth=0.45,alpha=1,zorder=1)
plt.plot(years,smoothed[:,1],linewidth=2,linestyle='--',
         dashes=(1, 0.2),color=cmocean.cm.phase(0.2),
         label=r'\textbf{Lowess Smoothing}',zorder=5)
plt.plot(years,spl(timearray),linewidth=2,linestyle='--',
         dashes=(1, 0.2),color=cmocean.cm.phase(0.6),
         label=r'\textbf{Spline Smoothing}',zorder=4)
plt.plot(years,p(timearray),linewidth=2,linestyle='--',
         dashes=(1, 0.2),color=cmocean.cm.phase(0.8),
         label=r'\textbf{Polynomial-6}',zorder=3)
plt.plot(years,gau,linewidth=2,linestyle='--',
         dashes=(1, 0.2),color=cmocean.cm.phase(1),
         label=r'\textbf{Gaussian}',zorder=2)

plt.xticks(np.arange(1850,2025,20),np.arange(1850,2025,20),rotation=0,
           fontsize=9)
plt.yticks(np.arange(-0.75,0.76,0.75),np.arange(-0.75,0.76,0.75),rotation=0,
           fontsize=9)
plt.xlim([1850,2018])
plt.ylim([-0.75,0.75])

l = plt.legend(shadow=False,fontsize=7.5,loc='upper center',
           bbox_to_anchor=(0.5, 1.1),fancybox=True,ncol=5,
            frameon=False)
for text in l.get_texts():
    text.set_color('darkgrey')

plt.savefig(directoryfigure + 'annualTemp_smoothing.png',dpi=300)

print('Completed: Script done!')