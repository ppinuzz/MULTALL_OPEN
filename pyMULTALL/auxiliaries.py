#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General auxiliary functions and objects, not related to a specific (sub)program.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import platform
from enum import Enum
from colorama import Fore, Style


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


class MessageLevel(Enum):
    """
    Enumeration of message formatting styles.
    
    Members
    -------
    ERROR
        Bright red error messages.
    WARNING
        Yellow warning messages.
    BASIC
        White (for black terminal) for basic messages and I/O.
    SUCCESS
        Bright green success messages.
    INFO
        Bright cyan information message (to attract user's attention).
    """
    
    # 2nd value is whether to use Style.BRIGHT or not
    # use bright red and bright green to have Spyder's red and green
    # (basic ones are hardly readable, the same goes for white)
    ERROR = (Fore.RED, True)
    WARNING = (Fore.YELLOW, False)
    BASIC = (Fore.WHITE, True)
    SUCCESS = (Fore.GREEN, True)
    INFO = (Fore.CYAN, True)


def print_message(message, level=MessageLevel.BASIC):
    """
    Helper to print user messages coloured based on their level.

    Parameters
    ----------
    message : str
        Message text, can be an f-string.
    level : MessageLevel, optional
        Message level controlling its colour. The default is MessageLevel.BASIC.

    Returns
    -------
    None.

    """
    
    color, bright = level.value
    if bright:
        style = Style.BRIGHT
    else:
        # empty string gets appended => no effect
        style = ''
    
    # Style.RESET_ALL stops subsequent text from being affected by these
    # color setups
    print(color + style + f'{message}' + Style.RESET_ALL)


if __name__ == '__main__':
    my_OS = get_OS_name()
    
    x = 12
    print_message(f'This x = {x} is a test, as {x**2} is', level=MessageLevel.INFO)