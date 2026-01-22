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
import pyMULTALL.auxiliaries as aux

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
    
    original_author_name = 'John D. Denton'
    original_author_email = 'jdd1@cam.ac.uk'
    print(f'Original author         : {original_author_name:15s}  {original_author_email}')
    print(f'Python code author      : {pyMULTALL.__author__[0]:15s}  {pyMULTALL.__email__[0]}')
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
    print(separator)
    print(f'Thermodynamic backend (for real gas model) : {pyMULTALL.defaults.THERMO_BACKEND}')
    if pyMULTALL.defaults.THERMO_BACKEND == 'REFPROP':
        if pyMULTALL.defaults.REFPROP_PATH is None:
            aux.print_message("No environmental variable 'RPPREFIX' was found, CoolProp may not be able to load REFPROP", aux.MessageLevel.BASIC)
        else:
            print(f'REFPROP path : {pyMULTALL.defaults.REFPROP_PATH}')
    print(separator)
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
    machine = input('Is this a compressor or a turbine? [c/t]')
    match machine.lower():
        case 'c':
            machine = 'compressor'
        case 't':
            machine = 'turbine'
        case _:
            raise ValueError(f"Unknown machine '{machine}'")
    input_data['machine'] = machine
    
    flow_type = input('Do you want to design: '
                      '\n\t AXI) an axial flow machine with a constant radius at a fixed spanwise position on each stage?' 
                      '\n\t MIX) a mixed flow machine with significant changes in radius through the stage? \n'
                      'Machine flow type [axi/mix]: ')
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
    
    input_data['gas_properties'] = {}
    gas_model = input('Gas model:'
                      '\n\t P) perfect' 
                      '\n\t I) ideal' 
                      '\n\t R) real'
                      '\n\t U) user-defined \n'
                      'Selected gas model [p/i/r/u]: ')
    match gas_model.lower():
        case 'p':
            gas_model = pyMULTALL.auxiliaries.GasModel.PERFECT
        case 'i':
            gas_model = pyMULTALL.auxiliaries.GasModel.IDEAL
        case 'r':
            gas_model = pyMULTALL.auxiliaries.GasModel.REAL
        case 'u':
            gas_model = pyMULTALL.auxiliaries.GasModel.USER_DEFINED
            raise NotImplementedError('User-defined gas models are not ready yet!')
        case _:
            raise ValueError('Unknown gas model')
    input_data['gas_properties']['model'] = gas_model
    
    # some of the following properties are not always needed/well-defined,
    # depending on the model
    if gas_model != pyMULTALL.auxiliaries.GasModel.REAL:
        R_gas = float(input('Massic gas constant [J/(kgK)]: '))
        if R_gas <= 0:
            raise ValueError('Massic gas constant cannot be zero or negative')
    else:
        R_gas = None
    input_data['gas_properties']['gas_constant'] = R_gas
    
    if gas_model == pyMULTALL.auxiliaries.GasModel.PERFECT:
        gamma_pv = float(input('Specific heat ratio Cp/Cv (i.e. gamma_pv): '))
        if gamma_pv <= 0:
            raise ValueError('Specific heat ratio (gamma_pv) cannot be zero or negative')
    else:
        gamma_pv = None
    input_data['gas_properties']['gamma'] = gamma_pv
    
    if gas_model == pyMULTALL.auxiliaries.GasModel.REAL:
        fluid = input('Fluid name (as in the thermodynamic backend): ')
    else:
        fluid = None
    input_data['gas_properties']['fluid'] = fluid
    
    N_stages = int(input('Number of stages in the machine: '))
    if N_stages <= 0:
        raise ValueError('A machine must have at least one stage')
    input_data['N_stages'] = N_stages
    
    ref_radius = input('Which radius do you want to use as a reference for the design:'
                       '\n\t H) hub'
                       '\n\t M) midspan'
                       '\n\t T) tip \n'
                       'Reference radius [h/m/t]: ')
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
        raise ValueError('Rotational speed cannot be zero or negative')
    input_data['rotation_speed'] = rotation_speed
    
    mass_flow_rate = float(input('Total mass flow rate [kg/s]: '))
    if mass_flow_rate <= 0:
        raise ValueError('Mass flow rate cannot be negative')
    input_data['mass_flow_rate'] = mass_flow_rate
    
    
    # ------------------------------ STAGE DATA ------------------------------
    # each stage has its number as key, from 1 to N_stages
    input_data['stages'] = {i: None for i in range(1, N_stages+1)}
    for i in range(1, N_stages+1):
        stage_data = {}
        print(f'Starting stage number {i}')
        
        if i > 1:
            equal_stage = print('Are the angles, mass flow rate, design radius, isentropic efficiency, etc. for this stage the same as for the previous stage [y/n]?')
            match equal_stage.lower():
                case 'y':
                    equal_stage = True
                case 'n':
                    equal_stage = False
                case _:
                    raise ValueError(f"Unknown answer '{equal_stage}'")
        else:
            # if this is the 1st stage, there's not prior stage that can be
            # equal to this one
            equal_stage = False
        stage_data['equal_stage'] = equal_stage
        
        # TODO: not yet 100% sure I got this...
        if flow_type == 'axial':
            flow_new = 'mixed'
        else:
            flow_new = 'axial'
        change_flow_stage = input(f'Do you want to change this stage from a(n) {flow_type} flow stage to a(n) {flow_new} flow stage [y/n]?')
        match change_flow_stage.lower():
            case 'y':
                change_flow_stage = True
                stage_flow_type = flow_new
            case 'n':
                change_flow_stage = False
                stage_flow_type = flow_type
            case _:
                raise ValueError(f"Unknown answer '{change_flow_stage}'")
        stage_data['stage_flow_type'] = stage_flow_type
        
        
        # MIXED FLOW STAGE PARAMETERS
        if flow_type == 'mixed':
            input_method = input('For MIXED flow machines, two input methods are available: '
                                 '\n\t A) input all 4 blade angles'
                                 '\n\t B) input the absolute flow angles at stage inlet and outlet and the flow coefficient (phi) and stage loading coefficient (psi)'
                                 '\n Design method [a/b]: ')
            match input_method.lower():
                case 'a':
                    input_method = 'blade_angles'
                case 'b':
                    input_method = 'angles_phi_psi'
                case _:
                    raise ValueError(f"Unknown input method '{input_method}'")
            stage_data['input_method'] = input_method
            
            match input_method:
                case 'blade_angles':
                    alpha_in_stat = float(input('Stator inlet flow angle [deg]: '))
                    if abs(alpha_in_stat) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['alpha_stator_in'] = alpha_in_stat
                    
                    alpha_out_stat = float(input('Stator outlet flow angle [deg]: '))
                    if abs(alpha_out_stat) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['alpha_stator_out'] = alpha_out_stat
                    
                    beta_in_rot = float(input('Rotor relative inlet flow angle [deg]: '))
                    if abs(beta_in_rot) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['beta_rotor_in'] = beta_in_rot
                    
                    beta_out_rot = float(input('Rotor relative outlet flow angle [deg]: '))
                    if abs(beta_out_rot) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['beta_rotor_out'] = beta_out_rot
                case 'angles_phi_psi':
                    if i == 1:
                        phi_first_rot_LE = float(input('Flow coefficient at the 1st rotor leading edge: '))
                        if phi_first_rot_LE <= 0:
                            raise ValueError('Flow coefficient cannot be zero or negative')
                        stage_data['phi_first_rotor_LE'] = phi_first_rot_LE
                
                    alpha_in_stage = float(input('Stage inlet absolute flow angle [deg]: '))
                    if abs(alpha_in_stage) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['alpha_in_stage'] = alpha_in_stage
                    
                    alpha_out_stage = float(input('Stage outlet absolute flow angle [deg]: '))
                    if abs(alpha_out_stage) > 90:
                        raise ValueError('All flow angles must lie in the range [-90, +90] deg')
                    stage_data['alpha_out_stage'] = alpha_out_stage
                    
                    psi_stage = float(input('Stage loading coefficient based on blade speed ar rotor leading edge: '))
                    if abs(psi_stage) < 0:
                        raise ValueError('The stage loading coefficient cannot be zero or negative')
                    stage_data['psi_rotor_LE'] = psi_stage
            
            # "mesh numerics"
            print('Input the stream surface coordinates and the meridional velocity ratios')
            print('The new values must form a smooth continuation of the last stream surface')
            if i == 0:
                N_pts_stream_surf = float(input('Number of points (i.e. axial coordinates) on the mean stream surface: '))
            else:
                use_old_points_number = input("The previous mean stream surface had {input_data['stages'][i-1]['N_points_stream_surface']} points on it, do you want to use that same number of points now [y/n]?")
                match use_old_points_number.lower():
                    case 'y':
                        N_pts_stream_surf = input_data['stages'][i-1]['N_points_stream_surface']
                    case 'n':
                        N_pts_stream_surf = float(input('Number of points (i.e. axial coordinates) on the mean stream surface: '))
                    case _:
                        raise ValueError(f"Unknown answer '{use_old_points_number}'")
            if N_pts_stream_surf <= 0:
                raise ValueError('The number of points on the mean stream surface cannot be zero or negative')
            stage_data['N_points_stream_surface'] = N_pts_stream_surf
            
            
            
        
        # .copy() to avoid shallow copying it and changing it
        input_data['stages'][i] = stage_data.copy()
    
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