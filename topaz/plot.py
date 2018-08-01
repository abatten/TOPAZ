#!/usr/bin/env python
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

import weight
import history

mpl.rc("xtick", labelsize=12)
mpl.rc("ytick", labelsize=12)
mpl.rc("font", size=16, family="serif",
       serif=[r"cmr10"], style="normal",
       variant="normal", stretch="normal")
mpl.rcParams["axes.unicode_minus"] = False
plt.rcParams['text.usetex'] = True


def rho_slice(sim, resolution=1000, cmap="inferno",
              units="Msol kpc^-3", show_cbar=False, **kwargs):
    """
    Make a density slice plot
    """
    
    redshift = sim.properties['Redshift']
    boxsize = sim.properties["boxsize"]

    im = pn.plot.image(sim.g, width=boxsize, resolution=resolution, 
                       cmap=cmap, units=units, show_cbar=show_cbar, **kwargs)
 
    if not show_cbar:
        cbar = plt.colorbar()
        cbar.set_label(label=r"$\rho\ [\mathrm{M_\odot\ kpc^{-3}}]$", fontsize=20)
    
    plt.ylabel(r"$y\ [\mathrm{cMpc}]$", fontsize=20)
    plt.xlabel(r"$x\ [\mathrm{cMpc}]$", fontsize=20)
    plt.title(r"$z = {0: .3f}$".format(redshift), fontsize=20)

    return(im)


def rho_proj(sim, resolution=1000, cmap="inferno", 
             units="Msol kpc^-2", show_cbar=False, **kwargs):
 
    redshift = sim.properties['Redshift']
    boxsize = sim.properties["boxsize"]
 
    im = pn.plot.image(sim.g, width=boxsize, resolution=resolution, 
                       cmap=cmap, units=units, show_cbar=show_cbar, **kwargs)
 
    if not show_cbar:
        cbar = plt.colorbar()
        cbar.set_label(label=r"$\rho\ [\mathrm{M_\odot\ kpc^{-2}}]$", fontsize=20)

    plt.ylabel(r"$y\ [\mathrm{cMpc}]$", fontsize=20)
    plt.xlabel(r"$x\ [\mathrm{cMpc}]$", fontsize=20)
    plt.title(r"$z = {0: .3f}$".format(redshift), fontsize=20)

    return(im)


def ion_history(redshifts=None, ion_history=None, snapshots=None, 
                ion="HI", weighting="volume", half_line=False,
                verbose=False, **kwargs):

    if snapshots is not None:
        redshifts, ion_history = history.weighted_mean(snapshots, ion,  weighting, verbose)

    if ion_history is None and redshifts is None:
        print("If HI history and redshifts are not provided, then snapshots must be.")
        print(" ")
        sys.exit(1)

    fig, ax = plt.subplots(1, figsize=(6, 4))

    ax.plot(redshifts, ion_history, "-b", label=r"Aurora")

    if half_line:
        # 50% ionised horizontal line
        ax.axhline(0.5, 0, 1, color='grey', linestyle='dashed', linewidth=1)

    ax.set_xlabel(r"$\mathrm{Redshift}$", fontsize=20)
    ax.set_ylabel(r"$<x_\mathrm{{{0}}}>$".format(ion), fontsize=20)
    plt.legend(fontsize=14, frameon=False)

    return(fig, ax)
