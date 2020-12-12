"""
Calculate steric height from regions of llc4320


Usage:
======  
   python c_dyn.py pth_to_the_region_folder

The program will create a folder named "dyn" for the calculated steric height.

The files share the same file format as the Theta and Salt files. 

A point of reference for the speed: the program uses about 0.8 minute to calculate one snapshot of CalCoast region (960x1754x88). 

Note that the jmd95 package used for the density calcualtion is a part of the MITgcm tool box. 

Example (pleiades):
=========================
module load python/2.7.15
cd /u/dmeneme/llc_4320/regions/
python c_dyn.py CalSWOT2

------------------------------------
Jinbo Wang (Jinbo.Wang@jpl.nasa.gov)
3/29/2019
------------------------------------
"""

import sys
sys.path.append('/u/jwang23/local/gsw-3.0.3/')
sys.path.append('/u/jwang23/local/popy/')

import glob,os
import gsw as sw
import popy

def calc(fnt,fns,fnout):
    """

     Load theta and salt data from fnt, fns
     Calculate density and steric height at each level integrated from the surface z=0
     Note that the free surface Eta is not included in the calculation. 

     Parameter: 
     fnt: the file name of theta
     fns: the file name of salt

    """

    s=np.memmap(fns,'>f4',mode='r',shape=(nz,nxy))
    t=np.memmap(fnt,'>f4',mode='r',shape=(nz,nxy))
    dens=popy.jmd95.densjmd95(s,t,pres)
    rho0=1027.5
    g=9.81
    (-((dens-rho0)/rho0*drf).cumsum(axis=0)).astype('>f4').tofile(fnout)
    del s,t,dens

    return

if __name__=='__main__':
    import time    
    import numpy as np
    from glob import glob
    import sys,os

    pth=sys.argv[1]

    nz=88

    pth_common='/nobackupp2/dmenemen/llc_4320/grid/'
    rc=np.fromfile(pth_common+'RC.data','>f4')[:nz]
    drf=np.fromfile(pth_common+'DRF.data','>f4')[:nz]

    fns=glob(pth+'/grid/*')
    print fns

    #grid information

    for fn in fns:
        if 'hFacC' in fn:
            hfacc=np.fromfile(fn,dtype='>f4').reshape(nz,-1)
        if 'YC' in fn:
            lat0=np.fromfile(fn,dtype='>f4').mean()

    drf=drf.reshape(-1,1)*hfacc  #factor drf 
    nxy=drf.shape[-1]
    #pressure
    pres=sw.p_from_z(-rc,lat0).reshape(-1,1) #reshape for broadcast to theta and salt coordinate

    fn_salt=sorted(glob(pth+'/Salt/*'))
    fn_theta=sorted(glob(pth+'/Theta/*'))

    if len(fn_salt) != len(fn_theta):
        sys.error('make sure theta and salt files are the same')
    else:
        print('There are %i files'%len(fn_theta))

    try:
        os.mkdir(pth+'/dyn')
    except:
        pass

    t0=time.time()
    for i in range(len(fn_salt)):
        fnout=fn_theta[i].replace('Theta','dyn')
        calc(fn_theta[i],fn_salt[i],fnout)
        print('progress: %i/%i used time %f min'%(i,len(fn_salt),(time.time()-t0)/60.))
        
