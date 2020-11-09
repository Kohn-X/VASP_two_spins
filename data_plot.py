import os.path
import numpy as np
from matplotlib import rc
from pylab import *
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import map_coordinates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

#define font as serif! this font is good.
rc('font',family='times new roman')
#rc('font',family='serif', serif='times new roman')
rcParams['mathtext.fontset'] = 'stix' #'custom'
#rc('font', serif='times new roman')
# adjust the distance between tick and ticklabels
# set before the figure is created
rcParams['xtick.major.pad'] = 10
rcParams['ytick.major.pad'] = 10

###==========================================================================================
def PlotEband(ax,path,low,high,xticknum,xtickname,xlabel,yticknum,ytickname,ylabel,title,col):

	bands = np.load(path).T
	print("Plot band from EIGENVAL")

	nbnd,nkpt = bands.shape
	nbnd = nbnd-1

	for i in range(nbnd):
		if min(bands[i+1])>high or max(bands[i+1])<low:
			pass
		else:
			ax.plot(bands[0],bands[i+1],color=col,lw=1.5)

	#ax.minortricks_on()
	#ax.yaxis.set_minor_locator(AutoMinorLocator(4))
	#ax.tick_paras('both',length=8,width=1.8,which='major')
	#ax.tick_paras('both',length=4,width=1,which='major')

	ax.set_xlim(bands[0,0],bands[0,-1])
	ax.set_ylim(low,high)

	xticknum = bands[0,xticknum]             
	ax.set_xticks(xticknum)
	ax.set_xticklabels(xtickname,fontsize=20)
	ax.set_yticks(yticknum)
	ax.set_yticklabels(ytickname,fontsize=20)

	ax.set_xlabel(xlabel,fontsize=20)
	ax.xaxis.set_label_coords(0.5,-0.1)             #define the position of xlabel
	ax.set_ylabel(ylabel,fontsize=25)
	ax.yaxis.set_label_coords(-0.15,0.5)

	ax.set_title(title,y=1.02,fontsize=20)

	for i in xticknum[1:len(xticknum)-1]:                   # high symmetry points
		ax.axvline(i, color='black', ls=':', lw=1)      
	ax.axhline(0,color='black',ls=':',lw=1)                 # fermi level

	#ax.grid(True)

###=============================================
fig = plt.figure(figsize=(9,6))
spec = gridspec.GridSpec(nrows=1,ncols=2)
ax1 = fig.add_subplot(spec[0,0])
ax2 = fig.add_subplot(spec[0,1])
fig.tight_layout()
fig.subplots_adjust(left=0.12,right=0.95,bottom=0.10,top=0.90,hspace=0.15,wspace=0.15)

###=============================================
path1='./1band_cal/'

low = -6                  # energy window 
high = 6

yticknum = range(-6,7,2)
ytickname = map(str,yticknum)
ylabel = 'E$\minus$E$_\mathrm{F}$ (eV)'

xticknum = [0,30,60,89]
xtickname = ['$\Gamma$','K','M','$\Gamma$']
xlabel = ''

cols=['r','b']
tits=['FM NiBr$_2$ ($\\alpha$)','FM NiBr$_2$ ($\\beta$)']

PlotEband(ax1,path1+'EbandUp.npy',low,high,xticknum,xtickname,xlabel,yticknum,ytickname,ylabel,tits[0],cols[0])
PlotEband(ax2,path1+'EbandDown.npy',low,high,xticknum,xtickname,xlabel,yticknum,ytickname,'',tits[1],cols[1])

#plt.savefig('VSe2B.pdf',format='pdf')

plt.show()
