# sdf_shape_blending
use shape blending method to generate contious shape varying mcirostructure

1.   first transform the bianry image seed into distrance field (singed distance field) scikit-fmm

2. shape blending 
<p align="center">
  <img width="460" height="300" src="https://github.com/cchu92/sdf_shape_blending/blob/main/family.gif" alt="Openscad">
</p>

<p align="center">
  <img width="460" height="300" src="https://github.com/cchu92/sdf_shape_blending/blob/main/shapemix.gif">
</p>

3. smooth filtering  postreatment(Gussisin filter method is applied here,
$\sigma$ is used to control athe level  of smoothing, and it shouldbe relatively small.
After the multi-scale optimizaiotn,  the adjecent cell change slightly, then the filtering should have  negnigle influence on function of each cell. Its main purpose was to mitigate any discrepancies that might have arisen due to the aforementioned variations between cells.)
  
