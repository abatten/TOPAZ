from scipy.io import FortranFile
import numpy as np

def readf(loc, ion='h1',cloudy='hm12', verbose=False, log=False):
    
    if log:
        file = "".join([loc + ion + '_' + cloudy + "_log"])
    else:
        file = "".join([loc + ion + '_' + cloudy])
    
    if verbose:
        print("Reading ", ion, " with background ", cloudy)
        print("Open file", file)
    
    with FortranFile(file, 'r') as f:
        # Define the header array, 3 integers
        headertype = np.dtype([('nz', '<i4'), ('ntemp', '<i4'), ('nvel', '<i4')])
        headerarr = f.read_reals( dtype=headertype )

        # Sample size in the 3D grid
        nz = headerarr[0][0]
        ntemp = headerarr[0][1]
        nrho = headerarr[0][2]
        
        if verbose:
            print("Number of redshift intervals ", nz)
            print("Number of temperature intervals ", ntemp)
            print("Number of density intervals ", nrho)

        # Output the ionisation fractions for the 3D grid
        
        # First define the ion fraction array datatype
        ionbaltype = np.dtype( np.float32, (nz, ntemp, nrho) )    
    
        # Read it and reshape the desired array
        ionbal = f.read_reals( dtype=ionbaltype ).reshape([nz, ntemp, nrho], order='F')

        # Output the values for redshift, temp and rho that correspond to the grids in ionbal
        valtype = np.dtype( np.float32, (nz+ntemp+nrho) )   

        valarr = f.read_reals( dtype = valtype ).reshape([nz + ntemp + nrho], order='F')

        zarr = valarr[0:nz]
        tarr = valarr[nz: (nz + ntemp) ]
        rarr = valarr[(nz+ntemp) : (nz + ntemp+ nrho)]
 
        if not log:
            for i in range(3):
                if len(np.where(ionbal < 0)[i]) > 0:
                    raise Exception(ion + ": This is a log file without log in file name") 

return ionbal, zarr, tarr, rarr
