#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary MEANGEN functions.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import datetime
import platform
import socket
import pyMULTALL

def print_startup_message(len_separator=70):
    
    separator = len_separator * '-'
    title = _title_formatting('pyMULTALL-OPEN', separator)
    
    print(separator)
    print(title)
    print(separator)
    
    print(f'Original author         : {pyMULTALL.__author__[0]:15s}  {pyMULTALL.__email__[0]}')
    print(f'Python code author      : {pyMULTALL.__author__[1]:15s}  {pyMULTALL.__email__[1]}')
    print(f'Version                 : {pyMULTALL.__version__}')
    print(separator)
    # https://stackoverflow.com/a/18944849/17220538
    print(f'Code launched on : {datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}')
    #print(f'Code running on  : {OS_name}')
    # https://stackoverflow.com/a/799799/17220538
    print(f'Host name        : {socket.gethostname()}')
    print(f'Node name        : {platform.node()}')
    print(separator)
    print('MEANGEN will create a mean-line design dataset used as input to the '
          'blade design program STAGEN, which in turn will create a 3D dataset '
          'for the MULTALL-OPEN program')
    #print(f'Thermodynamic backend : {REFPROP_path}')
    #print(separator)
    #print(f'Input file       : {input_file}')
    #print(f'Output directory : {output_dir}')
    #print(f'Log file         : {log_file}')
    #print(separator)
    
    #input_data = data_initial_message['input_data']
    #format_string = '\t{:<30s} : {:<10} {}'
        
    #print(format_string.format('Fluid', input_data['fluid'], ''))
    #print(format_string.format('T_tot @ inlet', input_data['total_inlet_temperature'], 'K'))
    # printing a True will print a 1, since bool's are instances of int's
    # https://discuss.python.org/t/bool-is-converted-to-int-in-an-f-string-is-this-supposed-to-happen/58008/3
    # convert to string to have 'True' or 'False'
    #print(format_string.format('Fixed geometry', str(input_data['use_fixed_geometry']), ''))



# ----------------------------- PRIVATE FUNCTIONS -----------------------------

def _title_formatting(title, separator):

    # if the entire line must be occupied by the title, the 2 space on the 
    # sides of the title, and the dashes, calculate how many dashes are left
    N_dashes = len(separator) - len(title) - 2
    # assuming the separator is composed of the same character, e.g. '-', 
    # repeated more than once => pick the separator char as separator[0]
    half_sep_title = round(N_dashes / 2) * separator[0]
    title = f'{half_sep_title} {title} {half_sep_title}'
    # the number of dashes has been rounded down, if the line is not long 
    # enough add dashes at the end of it
    delta_dashes = len(separator) - len(title)
    if delta_dashes > 0:
        title = title + delta_dashes * '-'
        
    return title