from sdf_operation import sdf_tStar,sdf_tref,sdf_smooth,sdf_mix_vf,design_weight
import  numpy as np 
import matplotlib.pyplot as plt

# load two sdf classses
geo1SDF = np.genfromtxt('curve1.csv', delimiter=',');
geo2SDF = np.genfromtxt('curve2.csv', delimiter=',');
SDF_list = [geo1SDF, geo2SDF]; 
nd = len(SDF_list)
weight = np.array([0.5,0.0]); # sum of the weright should be 1
# weight = np.array([0.5,0.4]); # sum of the weright should be 1
v_target = 0.05; # volume fraction of new sdf structure
sdf_mix=sdf_mix_vf(SDF_list,weight,v_target,Disp='True')


# plt.figure()
# plt.imshow(geo1SDF>0.1)
