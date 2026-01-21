#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Default values for global pyMULTALL parameters.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

from pathlib import Path
import os

# absolute path of the pyMULTALL package directory
PYMULTALL = Path(__file__).parent.resolve()

# thermodynamic backend: either 'HEOS' (CoolProp) or 'REFPROP'
THERMO_BACKEND = 'REFPROP'

# it seems that RPPREFIX is an evironment variable read by CoolProp to 
# locate REFPROP's executable (usually C:\Program Files (x86)\REFPROP)
# (unclear: do I need to define it, or is it created by CoolProp?)
# .get() returns None if not found
# https://stackoverflow.com/a/4907053/17220538
REFPROP_PATH = os.environ.get('RPPREFIX')
