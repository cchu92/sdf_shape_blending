import numpy as np



def sdf_tStar(DF,vfcommon):
    #   sdf_tStar: find the isovalue for a given volume fraction
    #   input:
    #       DF: signed distance field
    #       vfcommon: volume fraction
    #   output: 
    #       tStar: isovalue for the given volume fraction
    
   
    tstarguess = (np.max(DF) + np.min(DF))/2;
    errortal = 0.008
    binaDF = (DF>tstarguess).astype(np.int8)
    vf = np.mean(binaDF)
    errorvf = vf - vfcommon;
    move = 0.0001;
    # linear search 
    while np.abs(errorvf) > errortal:
        tstarguess = tstarguess + move*(errorvf/np.abs(errorvf));
        binaDF = (DF>tstarguess).astype(np.int8)
        vf = np.mean(binaDF)
        errorvf = vf - vfcommon
        print('vf,error:=: \{}'.format((vf,np.abs(errorvf))))
    return 0 - tstarguess
    

def sdf_tref(DF):
    from skimage import measure

    #   sdf_tref: find the low and up bound of the isovalue for a class of microstructure
    #   input:  
    #       DF: signed distance field
    #   output: 
    #       a: 2*1 array, the first element is the low bound of the isovalue, the second element is the up bound of the isovalue

    nb_connect = int(1);
    tref1 = (np.max(DF) + np.min(DF))/2; 
    tref2 = tref1;
    move = 0.001;
    vf = 1.0
    
    # low bound of tref
    while (nb_connect==1) and vf>0.1 :
        binaDF1 = (DF>tref1).astype(np.int8)
        vf = np.mean(binaDF1)
        nb_connect  = measure.label(binaDF1,connectivity=2, return_num='true')[1]
        tref1 = tref1+ move;

    tref1 = tref1 - move;
    
    # up bound of tref
    nb_connect = 1;
    vf =0;
    while (nb_connect==1) and vf<0.8 :
        binaDF2 = (DF>tref2).astype(np.int8)
        vf = np.mean(binaDF2)
        nb_connect  = measure.label(binaDF2,connectivity=2, return_num='true')[1]
        tref2 = tref2 - move
    tref2= tref2+move;
    a= np.array([0-tref1,0-tref2]);
   
    return a

def sdf_mix_vf(SDF,coeff,vftarget,tStar=None,trf=None,Disp = None):
    import matplotlib.pyplot as plt
    #   generate documentation for this function
    #   sdf_mix_vf: generate a mixed sdf with given volume fraction
    #   input:  
    #       SDF: a list of sdf, each sdf is a 2D array
    #       coeff: a list of coefficient for each sdf
    #       vftarget: target volume fraction
    #       tStar: a list of isovalue for each sdf
    #       trf: a list of low and up bound of isovalue for each sdf
    #   output: 
    #       f: mixed sdf with given volume fraction
   
    
    def projectHeaviside(x, HeavBeta, HeavEta):
        HeavDenom = np.tanh(HeavBeta*HeavEta) + np.tanh(HeavBeta*(1-HeavEta))
        filtered = (np.tanh(HeavBeta*HeavEta) + np.tanh(HeavBeta*(np.array(x)-HeavEta))) / HeavDenom
        return filtered
 
          
    def sdf_mix(SDF,coeff,tStar,trf,beta2,t):
        # %% step1 naive weighed sum of basis structure
        nFams = len(SDF)
        fWSum = -1e-9 # avid sigunarity  
        
        for dd in range(nFams):
                fWSum = fWSum + coeff[dd]* (SDF[dd]+ tStar[dd]); 

        fWSum = fWSum + t # inner isoval version
        fInner0 = np.exp( beta2*fWSum ); 
        # %% step 2: softmax union with lowest feasible unit cell of each basis class
        eta2 = np.percentile(coeff,80)-5e-2; 
        actv = projectHeaviside(np.array(coeff),128,eta2); 
        
        
        for dd in range(nFams):
            flow  = SDF[dd] + trf[dd,0]; 
            fInner0 = fInner0 + actv[dd] * np.exp( beta2*flow ); 
            
            
        f = np.log(fInner0) / beta2; 
        return f
    
    
            
    nFams = len(SDF);beta2 = 32; error = 1;t = -0.1; ervftol = 0.008; 
    move = 0.001
    if ((tStar is None) or (trf is None)):
        tStar = np.zeros((nFams,1)); # isovalue for each sdf guraate volume fraction 
        trf = np.zeros((nFams,2)); # up and low bound iso-value to
        for ii in range(nFams):
            tStar[ii,] =  sdf_tStar(SDF[ii],vftarget); 
            trf[ii,:] =  sdf_tref(SDF[ii]); 
            
    
    f = sdf_mix(SDF,coeff,tStar,trf,beta2,0.0)
    isov = sdf_tStar(f,vftarget);
    f = f + isov; 
    # while (np.abs(error)>ervftol):
    #     f = sdf_mix(SDF,coeff,tStar,trf,beta2,t)
    #     fbinary = (f>0).astype(np.int8)
    #     vf = np.mean(fbinary)
    #     error = vf - vftarget
    #     t = t - move*(error/abs(error)); 
    #     print('t:\{}'.format(t))
        
    if Disp is not None:
        plt.imshow((f>0.00).astype(np.int8), cmap='binary', vmin=0, vmax=1, aspect='equal')
        plt.title('Satisfy volume fraction target: vf={}'.format(np.mean((f>0).astype(np.int8))))
        # plt.show();
        
    
    return f 

def sdf_smooth(DF,sigma_var):
    from scipy.ndimage import gaussian_filter
    DF_smooth = gaussian_filter(DF, sigma=sigma_var)
    return DF_smooth



def design_weight(n,resolution):
    import numpy as np
    # input, interger diension
    # import numpy as np
    # Define the range of w1, w2, ..., wn values
    w_range = np.linspace(0, 1, num=resolution)

    # Create a n-dimensional grid of w1, w2, ..., wn values
    w_grid = np.meshgrid(*([w_range]*n))

    # Define a mask to select only the points that satisfy w1+w2+...+wn=1
    mask = np.sum(w_grid, axis=0) == 1

    # Select only the points that satisfy the mask
    w = np.stack([w_grid[i][mask] for i in range(n)], axis=1)
 
    return  w