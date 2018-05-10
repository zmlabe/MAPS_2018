"""
Script plots the global temperatures from various data sets

Notes
-----
    Author : Zachary Labe
    Date   : 7 May 2018
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

### Calculate multi-dataset mean for annual global temperatures    
meant = np.nanmean(annual,axis=0)

### Calculate multi-dataset mean for monthly global temperatures    
meanmonth = np.nanmean(data,axis=0)

filesave1 = False
if filesave1 == True:  
    np.savetxt(directorydata + 'annual_globaltemps.txt',annual.transpose(),
               delimiter=',',fmt='%3.2f',header='  '.join(datasets)+'\n',
               footer='\n File contains annual global surface temperatures' \
               '\n for hadcrut4, NASA, NOAA, BEST, and C&W',newline='\n\n')
filesave2 = False
if filesave2 == True:  
    np.savetxt(directorydata + 'annual_mean_globaltemps.txt',meant,
               delimiter=',',fmt='%3.2f',
               footer='\n File contains annual global surface temperatures' \
               '\n for *average* of hadcrut4, NASA, NOAA, BEST, and C&W',
               newline='\n\n')
filesave3 = False
if filesave3 == True:  
    np.savetxt(directorydata + 'monthly_mean_globaltemps.txt',meanmonth,
               delimiter=',',fmt='%3.2f',
               footer='\n File contains monthly global surface temperatures' \
               '\n for *average* of hadcrut4, NASA, NOAA, BEST, and C&W',
               newline='\n\n')

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
            spine.set_position(('outward', 5))
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

plt.axhline(y=0,color='darkgrey',linestyle=':',dashes=(1,0.3),linewidth=2)

color=iter(cmocean.cm.thermal(np.linspace(0.15,1,len(data))))
for i in range(data.shape[0]):
    cma=next(color)
    plt.plot(years,annual[i,:],color=cma,alpha=1,linewidth=1.5,
             label=datasets[i])
    
plt.xticks(np.arange(1850,2025,20),np.arange(1850,2025,20),rotation=0,fontsize=9)
plt.yticks(np.arange(-1,1.1,0.5),np.arange(-1,1.1,0.5),rotation=0,fontsize=9)
plt.xlim([1850,2018])
plt.ylim([-1,1])

l = plt.legend(shadow=False,fontsize=6.5,loc='lower center',
           bbox_to_anchor=(0.5, -0.025),fancybox=True,ncol=5,
            frameon=False)
for text in l.get_texts():
    text.set_color('darkgrey') 

plt.savefig(directoryfigure + 'annual_globaltemps.png',dpi=300)
