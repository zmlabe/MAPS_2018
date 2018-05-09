"""
Script plots the multi-observational data set mean to demonstrate changing
linear trends

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
print('\n' '----Plotting global temperature trends - %s----\n' % titletime)

### Alott time series
year1 = 1850
year2 = 2017
years = np.arange(year1,year2+1,1)

### Read in mean observational global surface temperature data
temp = np.genfromtxt(directorydata + 'annual_mean_globaltemps.txt',
                     unpack=True)
print('Completed: Read data!')

### Length of moving linear trend
length = 167

### Calculate moving linear trends
def calcLinearTrend(data,years,length):
    """
    Calculates moving linear trend for n length of years
    
    Parameters
    ----------
    data : 1d array
        [time series data]
    years : 1d array
        [years]
    length : integer
        [n years]
        
    Returns
    -------
    yearn : 2d array
        [years, years]
    trend : 2d array
        [A coefficient, B coefficient]
    
    Usage
    -----
    yearn,trend = calcLinearTrend(data,years,length)
    """
    print('\n>>> Using calcLinearTrend function!')
    
    ### Calculate moving trend using polyfit (1 degree)
    yearn = np.empty((data.shape[0]-length,length))
    trendn = np.empty((data.shape[0]-length,length))
    for i in range(data.shape[0]-length):
        yearn[i,:] = np.arange(years[i],years[i]+length,1)
        trendn[i,:] = data[i:i+length]
    
    trend = np.empty((data.shape[0]-length,2))  
    for i in range(data.shape[0]-length):
        trend[i,:] = np.polyfit(yearn[i],trendn[i],1)
    print('Completed: *%s YEAR* trends!' % length)
    
    print('*Completed: Finished calcLinearTrend function!\n')    
    return yearn,trend

### Calculate functions
yearn,trend = calcLinearTrend(temp,years,length)

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

plt.plot(years,temp,color='deepskyblue',alpha=1,linewidth=2)
for i in range(temp.shape[0]-length):
    plt.plot(yearn[i],trend[i,0]*yearn[i]+trend[i,1],
             color='orangered',linewidth=1)
    
plt.xticks(np.arange(1850,2025,20),np.arange(1850,2025,20),rotation=0,fontsize=9)
plt.yticks(np.arange(-0.75,0.76,0.75),np.arange(-0.75,0.76,0.75),rotation=0,fontsize=9)
plt.xlim([1850,2018])
plt.ylim([-0.75,0.75])

plt.text(1914,0.365,r'\textbf{\underline{%s}}' % length,color='orangered',fontsize=30,
         ha='right',va='center')
plt.text(1921,0.4,r'\textbf{Year}',color='orangered',fontsize=30,
         ha='left',va='center')

plt.savefig(directoryfigure + 'movingTrend_%s_year.png' % length,dpi=300)

        
