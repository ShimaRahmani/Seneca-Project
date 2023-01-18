#!/usr/bin/env python2

"""
Created on Wed Mar  1 17:29:34 2017

@author: duygu

"""

# from __future__ import print_function, absolute_import, division 

# import sys
# import os
# import math  as ma
# import numpy as np
# import scipy as sc

# import aemplots as pl

# import matplotlib.pyplot as plt
# import matplotlib.colors as col



import os
import sys
from sys import exit as error
from datetime import datetime
import warnings

import numpy as np

import matplotlib.collections
import matplotlib.patches
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib


nan        = float('NaN')
Fsize      = 13
Lsize      = 10.2
plotformat ='.png'

# Load observed data
#filename       = 'FWDModel_gtk4_3LRES5_thk15-25m.npz' 
#tmp            = np.load(filename)
#data_obs       = tmp['data_obs']  
#I_obs          = np.concatenate(([data_obs[:,0]], [data_obs[:,1]], [data_obs[:,2]], [data_obs[:,3]]))
#Q_obs          = np.concatenate(([data_obs[:,4]], [data_obs[:,5]], [data_obs[:,6]], [data_obs[:,7]]))

#filename='/home/bayats/work/AEM_Data/Tellus/data/Nearest/fwd_compare/Data_Clara_Line_A1_NM_intersection_FL11126/Test/models/SYNTH_AEM053Layer_Case3_60m_Perturb_50_nlyr32_TikhOpt_gcv_Results.npz' Duygu

filename="C:\\Users\\shima\\Desktop\\SYNTH_AEM05_3Layer_FinalTest_60m_Perturb_20_Volker_nlyr100_TikhOpt_gcv_Results.npz"
#filename='TIKH_results_BTML_L1455_Radar-less100m_block5.npz'
print (' Data read from '+filename)

FileName,filext0 = os.path.splitext(filename)
title=FileName
tmp = np.load(filename)

# ile=Fileout,
# fl_data=file,
# fl_name=fl_name,
# header=Header,
#mod_ref=tmp['mod_apr']
mod_act=tmp['mod_act']
# dat_act=dat_act,
site_modl=tmp['site_modl']
# site_modl_60m_0=site_modl[0]
# site_modl_60m_1=site_modl[1]
# site_modl_60m_2=site_modl[2]
# site_modl_60m_3=site_modl[3]
# site_modl_60m_4=site_modl[4]
# site_modl_60m_5=site_modl[5]
# site_modl_60m_6=site_modl[6]
# site_modl_60m_7=site_modl[7]
# site_modl_60m_8=site_modl[8]
# site_modl_60m_9=site_modl[9]
c=np.percentile(site_modl, 50, axis=0)



# site_merr=site_merr,
#site_dobs=site_dobs,
# site_dcal=site_dcal,
# site_derr=site_derr,
# site_nrms=site_nrms,
# site_nump=site_nump,
# site_num=site_num,
# site_y=site_y,
# site_x=site_x,
# site_gps=site_gps,
site_alt=tmp['site_alt']

dumm=np.shape(c)
nlyr=dumm[1]
# site_dem=site_dem)


res_true= np.array([100.0, 5.0, 100.0, 100.0]);
depthmax= 100; thk_true= np.array([15., 25., nan]);
dm= depthmax - np.sum(thk_true[:-1]);
depth= np.concatenate([[0],thk_true[:-1],[dm]]);
depthtrue= np.cumsum(depth);

#dz= tmp['dz']
#dzstart = .5
#dzend   = .5
#dz = np.logspace(dzstart,dzend,nlyr)
#z = np.append( 0., np.cumsum(dz)) 

# dzstart = 2.  somaye
# dzend = 10.
# dz = np.logspace(np.log10(dzstart), np.log10(dzend), nlyr)
# z = np.append(0.0, np.cumsum(dz))

#a=np.vstack((site_modl_60m_0[0:nlyr+1],site_modl_60m_1[0:nlyr+1],site_modl_60m_2[0:nlyr+1],site_modl_60m_3[0:nlyr+1], site_modl_60m_4[0:nlyr+1],site_modl_60m_5[0:nlyr+1],site_modl_60m_6[0:nlyr+1],site_modl_60m_7[0:nlyr+1],site_modl_60m_8[0:nlyr+1],site_modl_60m_9[0:nlyr+1]))
a=np.vstack((c[0:nlyr+1]))

# dzstart = 2.
# dzend = 10.
# # dz = numpy.logspace(numpy.log10(dzstart), numpy.log10(dzend), Nlyr)
# dz=np.zeros(75)+2
# z = np.append(0.0, np.cumsum(dz))

c=np.percentile(site_modl, 50, axis=0)


Nlyr = 100
dzstart = 2.
dzend = 10.
z =np.linspace(0, 100, Nlyr)
dz = np.zeros(Nlyr)+(z[1]-z[0])

#freq= np.array([912.0, 3005.0, 11962.0, 24510])

#plt.figure(1)
fig1 = plt.figure()
#ax1 = fig1.add_subplot(111) 
ax1 = fig1.add_subplot(111) 
#ax1.step(np.power(10.,site_modl_60m[1:nlyr+1]), -1*z[:-1], linewidth= .7, color= 'red', label='calculated model');
ax1.step(a[0], -1*z, linewidth= .7, color= 'red', label='calculated model');
for i in range(1,a.shape[0]):
    ax1.step(a[i], -1*z ,linewidth= .7, color= 'red');

#for n in sample_accptd:
#    res_edited = np.concatenate(([res_val[n,0]], [res_val[n,1]], [res_val[n,2]], [res_val[n,3]], [res_val[n,4]], [res_val[n,5]], [res_val[n,6]], [res_val[n,7]], [res_val[n,8]], [res_val[n,9]], [res_val[n,10]], [res_val[n,11]],[res_val[n,11]] ))
#    res_edited = np.power(10,res_edited)
#    ax1.step(res_edited[:], -1*depth_calc, linewidth= .7, color= [.75, .75, .75]);
plt.xscale('log')
plt.xlim([1,10000])
plt.ylim([-100, 0])
ax1.set_xlabel('resistivity ($\Omega$m)',fontsize=Fsize)
ax1.set_ylabel('depth (m)',fontsize=Fsize)

ax1.xaxis.set_label_position('top')
ax1.xaxis.set_ticks_position('both')
ax1.tick_params(labelsize=Lsize)


#    
ax1.step(res_true, -1*depthtrue, linewidth= 2.0, color= 'black', label= 'true model')
#ax1.step(np.power(10,med_res[:]), -1*depth_calc, linewidth= 2.0, color= 'red', label= 'median of accepted samples')
#ax1.step(np.power(10,prc_res_lower[:]), -1*depth_calc, linestyle= '--', linewidth=2.0, color= 'black')
#ax1.step(np.power(10,prc_res_upper[:]), -1*depth_calc, linestyle= '--', linewidth=2.0, color= 'black', label='95% quantiles')
ax1.legend(fontsize=12)
plt.grid(True)

# fig2 = plt.figure()
# ax2 =fig2.add_subplot(111)
# ax2.plot(freq, data_obs[:4], 'o', color= 'red', markersize=7, label='Obs_In-Phase')
# ax2.plot(freq, data_obs[4:8], 'o',  color= 'black', markersize=7, label='Obs_Quadrature')
# ax2.plot(freq, data_calc[:4], '-', color='red',markersize=7, label='Calc_In-Phase')
# ax2.plot(freq, data_calc[4:8], '-', color='black',markersize=7, label='Calc_Quadrature')
# ax2.set_xlabel('frequency (Hz)',fontsize=Fsize)
# ax2.xaxis.set_label_position('top')
# ax2.set_ylabel('data (ppm)',fontsize=Fsize)
# plt.xlim([100,100000])
# ax2.set_ylim([-100,3000])
# ax2.tick_params(labelsize=Lsize)
# plt.legend(loc='best', numpoints=1, fontsize=12)
# plt.xscale('log')
# plt.grid(True)
fig = plt.savefig(filename+plotformat)
plt.show()

