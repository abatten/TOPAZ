#!/usr/bin/env python
from __future__ import print_function, division

#  import numpy as np
#  from tqdm import tqdm
import trident
import yt


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


#  def rand_los(fn, output_data_dir, full_width=True):
#      if full_width:
#          ds = yt.load(fn)
#          width = ds.properties
#  
#  
#  def gen_n_los(dataset_file, n, rand=True):
#  
#      for i in range(n):
#          make_ray(dataset_file)
