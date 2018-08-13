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
from pynbody.snapshot.gadgethdf import SubFindHDFSnap
from pynbody.snapshot.gadgethdf import GadgetHDFSnap

from . import weight, history

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
        cbar.set_label(label=r"$\rho\ (\mathrm{M_\odot\ kpc^{-3}})$", fontsize=20)
    
    plt.ylabel(r"$y\ (\mathrm{cMpc})$", fontsize=20)
    plt.xlabel(r"$x\ (\mathrm{cMpc})$", fontsize=20)
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
        cbar.set_label(label=r"$\rho\ (\mathrm{M_\odot\ kpc^{-2}})$", fontsize=20)

    plt.ylabel(r"$y\ (\mathrm{cMpc})$", fontsize=20)
    plt.xlabel(r"$x\ (\mathrm{cMpc})$", fontsize=20)
    plt.title(r"$z = {0: .3f}$".format(redshift), fontsize=20)

    return(im)


def metal_map(sim, metal, **kwargs):
    redshift = sim.properties["Redshift"]
    metal_arr = sim.g[metal]
    metal_tot = np.sum(metal_arr)

    metallicity = "{0}XH".format(metal)
    if metal_tot != 0:
        im = sph.image(sim.g, qty=metallicity, width=sim.properties["boxsize"],
                  cmap="inferno", show_cbar=False, approximate_fast=False, 
                  **kwargs)
        cbar = plt.colorbar()
        cbar.set_label(label="[{0}/{1}]".format(metal, "H"), fontsize=16)
        plt.title("z = {1: .3f}".format(metal, redshift), fontsize=18)
        plt.ylabel(r"$y\ (\mathrm{cMpc})$", fontsize=16)
        plt.xlabel(r"$x\ (\mathrm{cMpc})$", fontsize=16)
    else:
        print("Zero metals found! Can not make metallicity \
              plot for: {0}".format(sim))

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



# There were taken from Pynbody gadgethdf.py 2018-08-13
XSOLH=0.70649785
XSOLHe=0.28055534
XSOLC=2.0665436E-3
XSOLN=8.3562563E-4
XSOLO=5.4926244E-3
XSOLNe=1.4144605E-3
XSOLMg=5.907064E-4
XSOLSi=6.825874E-4
XSOLS=4.0898522E-4
XSOLCa=6.4355E-5
XSOLFe=1.1032152E-3

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def CXH(sim):
    return (sim.g["C"] / sim.g["H"]) / (XSOLC/XSOLH)

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def HeXH(sim):
    return sim.g["He"] / sim.g["H"] / (XSOLHe/XSOLH)

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def FeXH(sim):
    return sim.g["Fe"] / sim.g["H"] / (XSOLFe/XSOLH) 

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def MgXH(sim):
    return sim.g["Mg"] / sim.g["H"] / (XSOLMg/XSOLH)

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def NXH(sim):
    return sim.g["N"] / sim.g["H"] / (XSOLN/XSOLH)

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def OXH(sim):
    return sim.g["O"] / sim.g["H"] / (XSOLO/XSOLH)

@GadgetHDFSnap.derived_quantity
@SubFindHDFSnap.derived_quantity
def SiXH(sim):
    return sim.g["Si"] / sim.g["H"] / (XSOLSi/XSOLH)
