#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General auxiliary functions and objects, not related to a specific (sub)program.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import platform
from enum import Enum


# create a custom exception to make the error message more meaningful
class UnrecognizedOSError(Exception):
    """Exception raised for unrecognized operating systems."""
    
    pass


class OperatingSystem(Enum):
    """
    Enumeration of supported operating systems.

    Members
    -------
    WINDOWS
        Microsoft Windows operating system.
    LINUX
        Linux-based operating systems.
    MAC
        Apple macOS (Darwin) operating system.
    """
    
    WINDOWS = 'windows'
    LINUX = 'linux'
    MAC = 'mac'


def get_OS_name():
    """
    Retrieve the name of the operating system: Windows, Linux or Mac OS.

    Raises
    ------
    UnrecognizedOSError
        If the OS cannot be determined.

    Returns
    -------
    OS_code : OperatingSystem
        The detected operating system.

    """
    
    # https://stackoverflow.com/a/58071295/17220538
    OS = platform.system()
    match OS:
        case 'Windows':
            OS_code = OperatingSystem.WINDOWS
        case 'Linux':
            OS_code = OperatingSystem.LINUX
        case 'Darwin':
            OS_code = OperatingSystem.MAC
        case _:
            raise UnrecognizedOSError('Unknown operating system')
    
    return OS_code


class GasModel(Enum):
    """
    Enumeration of supported gas models.
    
    Members
    -------
    PERFECT
        Perfect gas model (:math:`c_p =` const. and ideal gas law).
    IDEAL
        Ideal gas model (:math:`c_p = c_p(T)` and ideal gas law).
    REAL
        Real gas model (:math:`c_p = c_p(T, p)` and real gas relationship).
    USER_DEFINED
        User-defined (not implemented yet).
    """
    
    PERFECT = 'perfect'
    IDEAL = 'ideal'
    REAL = 'real'
    USER_DEFINED = 'user_defined'


if __name__ == '__main__':
    my_OS = get_OS_name()
