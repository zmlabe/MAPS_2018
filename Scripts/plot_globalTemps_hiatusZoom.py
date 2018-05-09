"""
Script plots the global temperatures from various data sets over the hiatus 
period

Notes
-----
    Author : Zachary Labe
    Date   : 9 May 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import nclcmaps as ncm
import datetime
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
print('\n' '----Plotting global temperatures - %s----' % titletime)

### Alott time series
year1 = 1850
year2 = 2017
years = np.arange(year1,year2+1,1)

datasets = [r'HadCRUT4',r'GISTEMP',r'NOAA',r'Berkeley',r'Cowtan \& Way']

### Read in data
filename = 'combined_temps_base_1971_to_2000.csv'
index,year,month,hadcru,giss,noaa,best,cowtan = np.genfromtxt(directorydata + \
                                                              filename,
                                                              unpack=True,
                                                              delimiter=',',
                                                              skip_header=1)

### Create array of temperatures
data = np.asarray([hadcru[:-12],giss[:-12],noaa[:-12],best[:-12],cowtan[:-12]])

### Calculate annual averages
N=12 # months
def groupedAvg(arrayq,N):
    result = np.nancumsum(arrayq,0)[N-1::N]/float(N)
    result[1:] = result[1:] - result[:-1]
    
    result[np.where(result==0)]=np.nan
    return result

annual = np.empty((5,years.shape[0]))
for i in range(data.shape[0]):
    annual[i] = groupedAvg(data[i],N)

### Calculate trends over the hiatus   
yearminh = 1998
yearmaxh = 2014
yearh = np.arange(1998,2014+1,1)
trends = np.empty((annual.shape[0],2))
for i in range(annual.shape[0]):
    hiatus = np.where((years >= yearminh) & (years <= yearmaxh))[0]
    annualq = annual[:,hiatus] 
    trends[i,:] = np.polyfit(yearh,annualq[i],1)
    
### Calculate multi-dataset mean
meant = np.nanmean(annual,axis=0)
trendmean = np.polyfit(yearh,meant[hiatus],1)

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
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params('both',length=5.5,width=2,which='major',direction='out')

color=iter(cmocean.cm.thermal(np.linspace(0.2,1,len(data))))
for i in range(data.shape[0]):
    cma=next(color)
    plt.plot(years,annual[i,:],color=cma,alpha=0.25,linewidth=3,
             label=datasets[i])
    plt.plot(yearh,yearh*trends[i,0]+trends[i,1],color=cma,alpha=0.3,
             linewidth=2.5,linestyle=':',dashes=(1,0.3))
    
plt.plot(yearh,yearh*trendmean[0]+trendmean[1],color='r',alpha=1,
         linewidth=3.5,linestyle=':',dashes=(1,0.3))
    
plt.xticks(np.arange(1850,2025,4),np.arange(1850,2025,4),rotation=0,fontsize=9)
plt.yticks(np.arange(0,0.81,0.1),np.arange(0,0.81,0.1),rotation=0,fontsize=9)
plt.xlim([1998,2014])
plt.ylim([0.1,0.6])

l = plt.legend(shadow=False,fontsize=6.5,loc='lower center',
           bbox_to_anchor=(0.5, -0.025),fancybox=True,ncol=5,
            frameon=False)
for text in l.get_texts():
    text.set_color('darkgrey') 

plt.savefig(directoryfigure + 'annual_globaltemps_zoomTrendMean.png',dpi=300)
