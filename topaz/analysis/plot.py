"""
A set of functions to plot stuff 
"""
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

mpl.rc("xtick", labelsize=12)
mpl.rc("ytick", labelsize=12)
mpl.rc("font", size=16,family="serif",
       serif=[r"cmr10"],style="normal",
       variant="normal",stretch="normal")
mpl.rcParams["axes.unicode_minus"] = False
plt.rcParams['text.usetex'] = True


def density_slice(sim):
    redshift = s.properties['Redshift']
    im = pn.plot.image(s.g, width=s.properties["boxsize"], resolution=1000, cmap="inferno", vmax=10**5, vmin=10**2.5, units = 'Msol kpc^-3', show_cbar=False)
    cbar = plt.colorbar()
    cbar.set_label(label=r"$\rho\ [\mathrm{M_\odot kpc^{-3}}]$", fontsize=20)
    plt.ylabel(r"$y\ [\mathrm{cMpc}]$", fontsize=20)
    plt.xlabel(r"$x\ [\mathrm{cMpc}]$", fontsize=20)
    plt.title(r"$z = {0: .3f}$".format(redshift), fontsize=20)

    return im
