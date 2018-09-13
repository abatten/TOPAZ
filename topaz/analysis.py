#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import pynbody as pn
from tqdm import tqdm


def weight(snapshot, qty, weight_type="volume"):
    """
    Weights the quantity 'qty' in the simulation.

    Parameters
    ----------

    snapshot : pynbody.snapshot

        The snapshot that will have its quantity weighted.

    qty : pynbody.array.SimArray
    
        The quantity to calculated the weighted. This is usually specified by
        using something similar to: s.g['rho']

    weight_type : {'mass', 'volume', None}, optional

        Which type of weighting to perform on the quantity. At the moment 
        mass weighting and no weighting are the same. This is corrent for 
        simulations where all the particles are the same mass.
        Default: 'volume'

    Returns
    -------

    weighted_qty : pynbody.array.SimArray
        The weighted quantity
    """
    if weight_type == "mass" or weight_type is None:
        pmass = snapshot.g["Mass"].in_units("m_p")
        total_mass = np.sum(pmass)
        weighted_quant = np.sum(qty * pmass / total_mass)

    elif weight_type == "volume":
        pmass = snapshot.g["Mass"].in_units("m_p")
        pvol = pmass / snapshot.g["Density"].in_units("m_p cm**-3")
        total_vol = np.sum(pvol)
        weighted_quant = np.sum(qty * pvol / total_vol)

    return weighted_qty


def ion_mean(snapshot_list, ion="HI", weighting=None, verbose=False, **kwargs):
    """
    Calculated the weighted mean fraction as a function of redshift.

    Parameters
    ----------
    snaplist : list of strings

        A list containing the paths for each snapshot.

    ion : string, optional

        The ion to calculate the weighted mean abundance.
        Options: HI, HeI, HeII (Default: HI)

    weighting : {'mass', 'volume', None}, optional

        The weighting scheme of the particles. Default: None

    verbose : boolean, optional

        If True, print progress information.
        (Default: False)

    Returns:
    --------
    redshift : numpy.darray

        A numpy array containing the redshifts of each snapshot.

    weighted_mean : numpy.darray

        The mean ion fraction at each of the redshifts
    """

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
