
# document for this module 


# python -m pydoc -w sdf_data

from sdf_operation import sdf_tref,sdf_tStar, sdf_mix_vf 
import numpy as np



# intilize the sdf_data class
class sdf_data:
    def __init__(dpp):
        dpp.nFams = []; # integer; number of  microstreucure classes
        dpp.SDF = []; # list: singed dsitance field for each classes
        dpp.tStar = []; # isovalue for each sdf guraate volume fraction 
        dpp.vf = []; 
        dpp.trf = []; # up and low bound iso-value to 
        dpp.fams  = [];
    def sdf_data_prepare(dpp,SDF,vf):
        # generate documentation for this function
        # sdf_data_prepare: prepare the data for sdf_data class
        # input:        
        #       SDF: a list of sdf, each sdf is a 2D array
        #       vf: volume fraction of the microstructure
        # output:       
        #       dpp: sdf_data class

        nFams = len(SDF); 
        dpp.nFams = nFams; 
        dpp.SDF = SDF; # list of singed distance field
        dpp.tStar = np.zeros((nFams,1)); # isovalue for each sdf guraate volume fraction 
        dpp.trf = np.zeros((nFams,2)); # up and low bound iso-value to 
        fam = np.arange(0,nFams,dtype='int'); 
        dpp.fams = fam; # 
        dpp.vf = vf; 

        for ii in range(dpp.nFams):
            dpp.tStar[ii,] =  sdf_tStar(dpp.SDF[ii],dpp.vf)
            dpp.trf[ii,:] = sdf_tref(dpp.SDF[ii])

    def sdf_data_geo(dpp,w):    
    
        # sdf_data_geo: generate the new sdf based on the weight
        # input:    
        #       w: weight for each sdf
        # output:
        #       SDF_new: new sdf
        #       SDF_new_trf: new sdf tref

        a1,b1 = w.shape
        SDF_new = []; 
        SDF_new_trf = np.zeros((a1,2))

        for ii in range(a1):
            # new sdf 
            coeff  = w[ii,:]# list 
            f = sdf_mix_vf(dpp.SDF,coeff,dpp.vf,dpp.tStar,dpp.trf)               
            SDF_new.append(f)
            SDF_new_trf[ii,:] = sdf_tref(f)
            
        dpp.SDF_new = SDF_new; 
        dpp.SDF_new_trf = SDF_new_trf; 
        return SDF_new, SDF_new_trf


# generate documnet for this module

    


    

    




