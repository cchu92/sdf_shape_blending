#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:10:08 2023

@author: 1321143263qq.com
"""

import yaml
import sdf_data
import sdf_operation
import numpy as np


geo1SDF = np.genfromtxt('curve5.csv', delimiter=',');
geo2SDF = np.genfromtxt('curve4.csv', delimiter=',');

SDF_list = [geo1SDF, geo2SDF]; 
resol = 30;
nd = len(SDF_list)
vf = 0.2
w = sdf_operation.design_weight(nd,resol)


# Get data from sdf_data module
dpp = sdf_data.sdf_data()
dpp.sdf_data_prepare(SDF_list, vf)

# Perform operation on data using sdf_operate function
DF_new, SDF_new_trf = dpp.sdf_data_geo(w)

# Create a dictionary with the result
yaml_dict = {"result": DF_new}


# yaml_dict = {"result": DF_new}

# Write the dictionary to a YAML file
with open("result.yaml", "w") as f:
    yaml.dump(yaml_dict, f)

# Read the YAML file
with open("result.yaml", "r") as f:
    yaml_dict = yaml.load(f, Loader=yaml.FullLoader)


# Print the result
print(yaml_dict)

# Path: sdf_data.py
# Compare this snippet from sdf_data.py:
#   def sdf_data_geo(dpp,w):
#         # sdf_data_geo: generate the new sdf based on the weight
#         # input:
#         #       w: weight for each sdf
#         # output:
#         #       SDF_new: new sdf
#         #       SDF_new_trf: new sdf tref
#      a1,b1 = w.shape
#      SDF_new = [];
#      SDF_new_trf = np.zeros((a1,2))
#      for ii in range(a1):
#          # new sdf
#          coeff  = w[ii,:]# list
#          f = sdf_mix_vf(dpp.SDF,coeff,dpp.vf,dpp.tStar,dpp.trf)
#          SDF_new.append(f)    
#          SDF_new_trf[ii,:] = sdf_tref(f)
#      dpp.SDF_new = SDF_new;
#      dpp.SDF_new_trf = SDF_new_trf;
#      return SDF_new, SDF_new_trf

# Path: sdf_data.py
# Compare this snippet from sdf_data.py:
#     def sdf_data_prepare(dpp,SDF,vf):
#         # sdf_data_prepare: prepare the data for sdf_data class
#         # input:
#         #       SDF: a list of sdf, each sdf is a 2D array
#         #       vf: volume fraction of the microstructure
#         # output:
#         #       dpp: sdf_data class
#         nFams = len(SDF);
#         dpp.nFams = nFams;
#         dpp.SDF = SDF; # list of singed distance field
#         dpp.tStar = np.zeros((nFams,1)); # isovalue for each sdf guraate volume fraction

#         dpp.trf = np.zeros((nFams,2)); # tref for each sdf
#         dpp.vf = vf; # volume fraction of the microstructure
#         for ii in range(nFams):

#             dpp.tStar[ii] = sdf_tstar(SDF[ii],vf)
#             dpp.trf[ii,:] = sdf_tref(SDF[ii])

#         dpp.SDF_new = [];
#         dpp.SDF_new_trf = [];

#         return dpp



