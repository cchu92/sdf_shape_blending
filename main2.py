from sdf_operation import sdf_tStar,sdf_tref,sdf_smooth,sdf_mix_vf,design_weight
import  numpy as np 


# load two sdf classses
geo1SDF = np.genfromtxt('curve5.csv', delimiter=',');
geo2SDF = np.genfromtxt('curve4.csv', delimiter=',');
SDF_list = [geo1SDF, geo2SDF]; 
nd = len(SDF_list)
weight = np.array([0.2,0.8]); # sum of the weright should be 1
v_target = 0.2; # volume fraction of new sdf structure
sdf_mix=sdf_mix_vf(SDF_list,weight,v_target,Disp='True')
