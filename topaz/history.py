#!/usr/bin/env python
from __future__ import print_function

import os
import imp
import sys
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy import units as u
import astropy.coordinates as coord

import pynbody as pn
import pynbody.analysis.profile as profile
import pynbody.analysis.cosmology as cosmology
import pynbody.plot.sph as sph
from tqdm import tqdm

from . import weight


def weighted_mean(snaplist, ion="HI", weighting=None, verbose=False, **kwargs):
    """
    Calculated the weighted mean fraction as a function of redshift.

    Parameters
    ----------
    snaplist : list of strings
        A list containing the paths for each snapshot.

    ion : string
        The ion to calculate the weighted mean abundance.
        Options: HI, HeI, HeII

    weighting : string or None
        The weighting scheme of the particles.
        "volume", "mass" or None (default)

    verbose : boolean
        If True, print progress information.
        False (default)

    Returns:
    --------
    redshift : numpy array
        The redshifts of the snapshots

    weighted_mean : numpy array
        The mean HI fraction at each of the redshifts
    """

    if verbose:
        print("****")
        print("Hang on tight, this could take a little while.")
        print("****")

    weighted_mean = []
    redshift = []

    for snap in tqdm(snaplist, desc=ion, disable=not verbose):
        snap_suffix = snap.split("_")[-1]
        snap_file = "{0}/snap_{1}".format(snap, snap_suffix)

        s = pn.load(snap_file)

        apion = "ap{0}".format(ion)

        if weighting == "volume":
            weighted_mean.append(weight.volume_weight(s, s.g[apion]))

        elif weighting == "mass" or weighting is None:
            weighted_mean.append(weight.mass_weight(s, s.g[apion]))

        redshift.append(s.properties["Redshift"])

    return np.array(redshift), np.array(weighted_mean)
