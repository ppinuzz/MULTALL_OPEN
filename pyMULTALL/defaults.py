#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Default values for global pyMULTALL parameters.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

from pathlib import Path

# absolute path of the pyMULTALL package directory
PYMULTALL = Path(__file__).parent.resolve()

# thermodynamic backend: either 'HEOS' (CoolProp) or 'REFPROP'
THERMO_BACKEND = 'REFPROP'