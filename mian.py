from sdf_operation import sdf_tStar,sdf_tref,sdf_smooth,sdf_mix_vf,design_weight
import numpy as np
import sdf_data 
import matplotlib.pyplot as plt


geo1SDF = np.genfromtxt('geoA_sdfs.csv', delimiter=',')
geo2SDF = np.genfromtxt('geoB_sdfs.csv', delimiter=',')



# SDF list
SDF_list = [geo1SDF, geo2SDF]; 
resol = 10;
nd = len(SDF_list)
w = design_weight(nd,resol)


# SDF OPERATION 
dpp = sdf_data.sdf_data()
dpp.sdf_data_prepare(SDF_list, 0.5)
DF_new, SDF_new_trf = dpp.sdf_data_geo(w)

# NEW STRUCTURE 
DF_new = np.hstack(DF_new)


sss = sdf_mix_vf(SDF_list,np.array([0.4,0.6]),0.3,Disp='True')


plt.figure
plt.imshow((DF_new>0.00).astype(np.int8), cmap='binary', vmin=0, vmax=1, aspect='equal')

# 

plt.figure(1)
smoothsdf = sdf_smooth(DF_new,8)
plt.imshow((smoothsdf>0.00).astype(np.int8), cmap='binary', vmin=0, vmax=1, aspect='equal')

plt.figure(2)
smoothsdf = sdf_smooth(DF_new,2)
plt.imshow((smoothsdf>0.00).astype(np.int8), cmap='binary', vmin=0, vmax=1, aspect='equal')

