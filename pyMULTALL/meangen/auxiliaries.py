#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary MEANGEN functions.

To test it, run python -m pyMULTALL.meangen.auxiliaries

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import datetime
import platform
import socket
import pyMULTALL

def print_startup_message(len_separator=70):
    """
    Print startup message with author names, date, version, ecc.

    Parameters
    ----------
    len_separator : int, optional
        Length of the separator string (the char ``-`` repeated more times). 
        The default is 70.

    Returns
    -------
    None.

    """
    
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


def interactive_input():
    """
    Ask the user for input interactively.

    Raises
    ------
    ValueError
        If an input parameter has an invalid value.

    Returns
    -------
    input_data : dict
        Input data, as-if read from a ``.yaml`` file.

    """
    
    # ----------------------------- GENERAL DATA -----------------------------
    input_data = {}
    machine = input('Is this a compressor (C) or a turbine (T)? ')
    match machine.lower():
        case 'c':
            machine = 'compressor'
        case 't':
            machine = 'turbine'
        case _:
            raise ValueError(f"Unknown machine '{machine}'")
    input_data['machine'] = machine
    
    flow_type = input('Do you want to design: \n\t AXI) an axial flow machine with a constant radius at a fixed spanwise position on each stage? \n\t MIX) a mixed flow machine with significant changes in radius through the stage? \n')
    match flow_type.lower():
        case 'axi':
            flow_type = 'axial'
        case 'mix':
            flow_type = 'mixed'
        case _:
            raise ValueError(f"Unknown machine flow type '{flow_type}'")
    input_data['machine_flow_type'] = flow_type
    
    print('Sign conventions: ')
    print('- The blade rotation must in the positive theta direction')
    print('- Flow angles are positive is the associated velocity vector has a tangential component in the positive theta direction (i.e. positive rotation direction)')
    
    input_data['inlet_conditions'] = {}
    p_tot_in = float(input('Inlet stagnation pressure [bar]: '))
    if p_tot_in <= 0:
        raise ValueError('Pressure cannot be zero or negative')
    input_data['inlet_conditions']['total_pressure'] = 1e5 * p_tot_in
    
    T_tot_in = float(input('Inlet stagnation temperature [K]: '))
    if T_tot_in <= 0:
        raise ValueError('Temperature cannot be zero or negative')
    input_data['inlet_conditions']['total_temperature'] = T_tot_in
    
    # TODO: insert gas constants and model
    
    N_stages = int(input('Number of stages in the machine: '))
    if N_stages <= 0:
        raise ValueError(f'A machine must have at least one stage')
    input_data['N_stages'] = N_stages
    
    ref_radius = input('Which radius do you want to use as a reference for the design: \n\t H) hub \n\t M) midspan \n\t T) tip \n')
    match ref_radius.lower():
        case 'h':
            ref_radius = 'hub'
        case 'm':
            ref_radius = 'midspan'
        case 't':
            ref_radius = 'tip'
        case _:
            raise ValueError(f"Unknown reference radius '{ref_radius}'")
    input_data['design_point_radius'] = ref_radius
    
    rotation_speed = float(input('Rotational speed [rpm]: '))
    if rotation_speed <= 0:
        raise ValueError(f'Rotational speed cannot be zero or negative')
    input_data['rotation_speed'] = rotation_speed
    
    mass_flow_rate = float(input('Total mass flow rate [kg/s]: '))
    if mass_flow_rate <= 0:
        raise ValueError(f'Mass flow rate cannot be negative')
    input_data['mass_flow_rate'] = mass_flow_rate
    
    
    # ------------------------------ STAGE DATA ------------------------------
    # each stage has its number as key, from 1 to N_stages
    input_data['stages'] = {i for i in range(1, N_stages+1)}
    for i in range(1, N_stages+1):
        print(f'Starting stage number {i}')
    
    return input_data


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


if __name__ == '__main__':
    interactive_input()