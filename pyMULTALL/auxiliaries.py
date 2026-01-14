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
    WINDOWS = 0
    LINUX = 1
    MAC = 3

def get_OS_name():
    
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
    PERFECT = 1


if __name__ == '__main__':
    
    my_OS = get_OS_name()