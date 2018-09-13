#!/usr/bin/env python
from __future__ import print_function, division

import numpy as np
from tqdm import tqdm
import trident
import yt

#yt.mylog.disabled = True
yt.funcs.mylog.setLevel(50)

def make_ray(dataset_file, ray_start, ray_end, line_list=["H I", "H II"],
             field_list=None, filename="ray.h5", return_ray=False,  **kwargs):
    """

    A wrapper for the trident.make_simple_ray function to generate rays in
    SPH simulations.

    Parameters
    ----------

    dataset_file : string or YT Dataset object

        Either a YT dataset object or the filename of a dataset on disk.

    ray_start, ray_end : list of floats

        The coordinates of the starting and end positions of the ray. The
        coordinates are assumed to be in code length units.

    line_list : list of strings, optional

        The list that will determine which fields that will be
        added to output ray. The format of these is important, they can
        include elements (e.g. "C" for Carbon), ions (e.g. "He II" for
        specifically the Helium II line) or wavelengths (e.g. "Mg II #####"
        where # is the integer wavelength of the line). These fields will
        appear in the output ray dataset in the form of "H_p0_number_density"
        (H plus 0 = H I). Default: ["H I", "H II"]

    field_list : list of string, optional

        The list of which additional fields to add to the output light ray.
        Default: None

    filename : string, optional

        The output file name for the ray data stored as a HDF5 file.
        The ray must be saved. Default: "ray.h5"

    return_ray : boolean, optional

        If true, make_ray will return the generated YTDataLightRayDataset,
        If false, make_ray will return None. Default: False


    Returns
    -------
    ray
        return_ray = True: Returns the generated YTDataLightRayDataset
    None
        return_ray = False: Returns None
    """

    # If supplied a path name, load the snapshot first
    if isinstance(dataset_file, str):
        ds = yt.load(dataset_file)
    else:
        ds = dataset_file

    if field_list is None:
        field_list = []

    field_list.extend([('PartType0', 'SmoothingLength'),
                       ('PartType0', 'ParticleIDs')])

    trident.add_ion_fields(ds, ions=line_list)

    ray = trident.make_simple_ray(ds,
                                  start_position=ray_start,
                                  end_position=ray_end,
                                  lines=line_list,
                                  ftype='PartType0',
                                  fields=field_list,
                                  data_filename=filename,
                                  **kwargs)
    if return_ray:
        return ray
    else:
        return None


def random_ray(dataset_file, output_data_dir="", axis="z",
               ray_prefix="Ray", return_ray=False):
    """
    Generate a ray with a random start and end point.

    """
    if isinstance(dataset_file, str):
        ds = yt.load(dataset_file)
    else:
        ds = dataset_file

    width = ds.parameters['BoxSize']

    #  Generate 2 random numbers for the coordinates of the rays
    rand_0 = round(np.random.uniform(low=0.0, high=1.0) * width, 2)
    rand_1 = round(np.random.uniform(low=0.0, high=1.0) * width, 2)

    #  Generate starting and end point for the rays
    if axis == "x":
        xi, yi, zi = 0.00, rand_0, rand_1
        xf, yf, zf = round(width, 2), rand_0, rand_1
        ray_start = [xi, yi, zi]
        ray_end = [xf, yf, zf]

    elif axis == "y":
        xi, yi, zi = rand_0, 0.00, rand_1
        xf, yf, zf = rand_0, round(width, 2), rand_1
        ray_start = [xi, yi, zi]
        ray_end = [xf, yf, zf]

    elif axis == "z":
        xi, yi, zi = rand_0, rand_1, 0.00
        xf, yf, zf = rand_0, rand_1, round(width, 2)
        ray_start = [xi, yi, zi]
        ray_end = [xf, yf, zf]

    #line_list = ["H I", "H II", "He I", "He II", "He III"]

    line_list = ["H", "He"]

    #  Determine which two axis to add to filename
    xyz = ["x", "y", "z"]
    xyz.remove(axis)

    filename = "{0}/{1}_{2}_{3}_{4}.h5".format(
        output_data_dir, ray_prefix, "_".join(line_list), axis + "axis",
        "_".join(["{0}{1}".format(xyz[0], rand_0),
        "{0}{1}".format(xyz[1], rand_1)]))
                                       
    ray = make_ray(ds, 
                   ray_start=ray_start,
                   ray_end=ray_end,
                   line_list=line_list,
                   filename=filename, 
                   return_ray=return_ray)
    
    if return_ray:
        return ray
    else:
        return None
  
  
def make_n_random_rays(dataset_file, n, output_data_dir, ray_prefix="Ray",
                       verbose=False):

    """
    Generate n random rays with the rays.random_ray function.

    Parameters
    ----------
    dataset_file : string or YT Dataset object
        
        Either a YT dataset object or the filename of a dataset on disk.

    n : integer

        The number of random rays to generate.

    output_data_dir : string
        
        The location on disk where the data from the generated rays will be
        saved as a HDF5 file.

    ray_prefix : optional, string
        
        The ray_prefix will becone the first part of the filename when the 
        rays are saved. Default: 'Ray'

    verbose : optional, boolean
        Default: False
    """

    for i in tqdm(range(n), desc="Generating Random Ray"):
        random_ray(dataset_file, 
                   output_data_dir, 
                   ray_prefix="Ray_Aurora_L012N0128",
                   return_ray=False)

    return None

        
