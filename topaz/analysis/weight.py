#!/usr/bin/env python
"""
Functions to calculate weighted averages
"""
from __future__ import print_function

import numpy as np

def volume_weight(sim, quant):
    """
    Volume weights the quantity 'quant' in the simulation.
    """
    pmass = sim.g["Mass"].in_units("m_p")
    pvol = pmass / sim.g["Density"].in_units("m_p cm**-3")

    total_vol = np.sum(pvol)

    vol_weighted_quant = np.sum(quant * pvol / total_vol)

    return vol_weighted_quant


def mass_weight(sim, quant):
    """
    Applied a mass weighting to the quantity 'quant' in the simulation.
    """
    pmass = sim.g["Mass"].in_units("m_p")

    total_mass = np.sum(pmass)

    mass_weighted_quant = np.sum(quant * pmass / total_mass)

    return mass_weighted_quant
