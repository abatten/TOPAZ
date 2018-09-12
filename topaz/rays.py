#!/usr/bin/env python
from __future__ import print_function, division

import numpy as np
from tqdm import tqdm
import trident


def gen_ray(fn, ray_start, ray_end, line_list=["H", "He"], 
            field_list=[], filename="ray.h5",  **kwargs):


    field_list.extend([('PartType0', 'SmoothingLength'),
                       ('PartType0', 'ParticleIDs')])

    ray = trident.make_simple_ray(fn, 
                                  start_position=ray_start,
                                  end_position=ray_end,
                                  lines=line_list,
                                  ftype='PartType0',
                                  fields=field_list,
                                  data_filename=filename)


def rand_los(fn, output_data_dir, full_width=True):
    if full_width:
        ds = yt.load(fn)
        width = ds.properties


def gen_n_los(fn, n, rand=True):

    for i in range(n):
        gen_los(fn,
                )
