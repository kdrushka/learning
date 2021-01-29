import glob
import re

# directories
datadir='/data1/adac/'
llc4320dir=datadir + 'mitgcm/regions/'
processdir=datadir + 'process/'


# open a new file
f = open(processdir + 'llc4320_regional_grids.txt', 'w')
# header
f.write('region,Nx,Ny,Nz\n')

# get grid info by parsing the hFacC file
for hf in glob.glob(llc4320dir + '/**/grid/hFacC**'):
#     print(hf)
    pat1=re.compile(r'regions/(.*)/grid/')
    REGION=pat1.search(hf).group(1)
    pattern=re.compile(r'hFacC_(.*)x(.*)x(.*)')
    nx=pattern.search(hf).group(1)
    ny=pattern.search(hf).group(2)
    nz=pattern.search(hf).group(3)
    print(REGION + ',' + nx + ',' + ny + ',' + nz)
    f.write(REGION + ',' + nx + ',' + ny + ',' + nz + '\n')
f.close()
