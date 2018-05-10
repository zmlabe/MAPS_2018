"""
Script plots the multi-observational data set mean to demonstrate changing
moving averages (# of months)

Notes
-----
    Author : Zachary Labe
    Date   : 10 May 2018
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
print('\n' '----Plotting global temperature averages - %s----\n' % titletime)

### Alott time series
year1 = 1850
year2 = 2017
years = np.arange(year1,year2+1,1)
months = np.arange(years.shape[0]*12)

### Read in mean observational global surface temperature data
temp = np.genfromtxt(directorydata + 'monthly_mean_globaltemps.txt',
                     unpack=True)
print('Completed: Read data!')

### Calculate moving linear trends
def calcLinearTrend(data,length):
    """
    Calculates moving average for n number of months
    
    Parameters
    ----------
    data : 1d array
        [time series data]
    length : integer
        [n months]
        
    Returns
    -------
    ave : 1d array
        time series of smoothed data from moving average
    
    Usage
    -----
    ave = calcLinearTrend(data,years,length)
    """
    print('\n>>> Using calcMovingAverage function!')
    
    ### Calculate moving average for n months (length)
    aven = np.convolve(data, np.ones((length,))/length, mode='valid') 
    print('Completed: *%s MONTHS* averages!' % length)
    
    ### Append nans for consistent time
    empty = np.array([np.nan]*(length-1))
    ave = np.append(empty,aven,axis=0)
    
    print('*Completed: Finished calcMovingAverage function!\n')    
    return ave

### Calculate functions
ave12 = calcLinearTrend(temp,12)
ave60 = calcLinearTrend(temp,60)
ave132 = calcLinearTrend(temp,132)

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

plt.plot(months,ave12,color='deepskyblue',linewidth=2,
         label=r'12-month',alpha=0.4,zorder=1)
plt.plot(months,ave60,color='lawngreen',linewidth=2,
         label=r'60-month',alpha=0.4,zorder=2)
plt.plot(months,ave132,color='m',linewidth=2.3,
         label=r'132-month',alpha=1,zorder=3)

plt.yticks(np.arange(-0.8,0.81,0.8),np.arange(-0.8,0.81,0.8),rotation=0,fontsize=9)
plt.ylim([-0.8,0.8])
plt.xlim([0,2016])

l = plt.legend(shadow=False,fontsize=7.5,loc='upper center',
           bbox_to_anchor=(0.5, 1.03),fancybox=True,ncol=5,
            frameon=False)
for text in l.get_texts():
    text.set_color('darkgrey')

plt.savefig(directoryfigure + 'movingAverageTemps_132.png',dpi=300)

print('Completed: Script done!')