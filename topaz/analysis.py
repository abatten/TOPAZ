#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import pynbody as pn
from tqdm import tqdm


def weight(sim, quant, weight_type="mass"):
    """
    Volume weights the quantity 'quant' in the simulation.
    """
    if weight_type == "mass" or weight_type is None:
        pmass = sim.g["Mass"].in_units("m_p")
        total_mass = np.sum(pmass)
        weighted_quant = np.sum(quant * pmass / total_mass)

    elif weight_type == "volume":
        pmass = sim.g["Mass"].in_units("m_p")
        pvol = pmass / sim.g["Density"].in_units("m_p cm**-3")
        total_vol = np.sum(pvol)
        weighted_quant = np.sum(quant * pvol / total_vol)

    return weighted_quant


def ion_mean(snaplist, ion="HI", weighting=None, verbose=False, **kwargs):
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
        weighted_mean.append(weight(s, s.g[apion], weight_type=weighting))
        redshift.append(s.properties["Redshift"])

    return np.array(redshift), np.array(weighted_mean)


def create_los(snapshot, ray_start, ray_end):
    return None
