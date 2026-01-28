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
import pyMULTALL.meangen.defaults as meangen_def
from prettytable import PrettyTable

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
    title = aux._title_formatting('pyMULTALL-OPEN', separator)
    
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
            aux.print_message("No environmental variable 'RPPREFIX' was found, CoolProp may not be able to load REFPROP", aux.MessageLevel.WARNING)
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
    
    aux.print_message('Sign conventions: '
          '\n\t - The blade rotation must in the positive theta direction'
          '\n\t - Flow angles are positive is the associated velocity vector has a tangential component in the positive theta direction (i.e. positive rotation direction)',
          aux.MessageLevel.INFO)
    
    input_data['inlet_conditions'] = {}
    p_tot_in = float(input('Inlet stagnation pressure [bar]: '))
    if p_tot_in <= 0:
        raise ValueError('Pressure cannot be zero or negative')
    # convert from bar to Pa
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
    # stage default values for some parameters
    stage_default = meangen_def.StageOpts()
    # each stage has its number as key, from 1 to N_stages
    input_data['stages'] = {i: None for i in range(1, N_stages+1)}
    for i in range(1, N_stages+1):
        stage_data = {}
        aux.print_message(f'Starting stage number {i}', aux.MessageLevel.INFO)
        
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
        stage_data['change_flow_type'] = change_flow_stage
        
        
        # MIXED FLOW STAGE PARAMETERS
        if change_flow_stage and stage_flow_type == 'mixed':
            aux.print_message('For MIXED flow machines, two input methods are available: '
                              '\n\t A) input all 4 blade angles'
                              '\n\t B) input the absolute flow angles at stage inlet and outlet and the flow coefficient (phi) and stage loading coefficient (psi)', 
                              aux.MessageLevel.INFO)
            
            input_method = input('Design method [a/b]: ')
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
            
            # STREAM SURFACE MESH NUMERICS
            # (while loop because in the original MEANGEN.17.4.f you were given
            # the possibility to change the stream surface coordinates after 
            # having given them, in case you made a mistake)
            change_stream_surf_coords = True
            while change_stream_surf_coords:
                print('Input the stream surface coordinates and the meridional velocity ratios')
                aux.print_message('The new values must form a smooth continuation of the last stream surface', 
                                  aux.MessageLevel.INFO)
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
                
                if i > 0:
                    print(f"Axial coordinates of the stream surface of the previous stage [m]: {input_data['stages'][i-1]['stream_surf_axial_coords']}")
                    use_old_axial_stream_coords = input('Use the axial stream surface coordinates of the previous stage also in this stage [y/n]? ')
                    match use_old_axial_stream_coords.lower():
                        case 'y':
                            axial_stream_coords = input_data['stages'][i-1]['stream_surf_axial_coords'].copy()
                        case 'n':
                            # returns a string '0.5 0.6 07' => split at spaces...
                            axial_stream_coords = input('Axial coordinates of the mean stream surface (space-separated) [m]: ').split()
                            # ... and turn each piece in a float
                            axial_stream_coords = list(map(float, axial_stream_coords))
                        case _:
                            raise ValueError(f"Unknown answer '{use_old_axial_stream_coords}'")
                    stage_data['stream_surf_axial_coords'] = axial_stream_coords.copy()
                    
                if i > 0:
                    print(f"Radial coordinates of the stream surface of the previous stage [m]: {input_data['stages'][i-1]['stream_surf_radial_coords']}")
                    use_old_radial_stream_coords = input('Use the radial stream surface coordinates of the previous stage also in this stage [y/n]? ')
                    match use_old_radial_stream_coords.lower():
                        case 'y':
                            radial_stream_coords = input_data['stages'][i-1]['stream_surf_radial_coords'].copy()
                        case 'n':
                            # returns a string '0.5 0.6 07' => split at spaces...
                            radial_stream_coords = input('Radial coordinates of the mean stream surface (space-separated) [m]: ').split()
                            # ... and turn each piece in a float
                            radial_stream_coords = list(map(float, radial_stream_coords))
                        case _:
                            raise ValueError(f"Unknown answer '{use_old_radial_stream_coords}'")
                    stage_data['stream_surf_radial_coords'] = radial_stream_coords.copy()
                    
                if i > 0:
                    print(f"Meridional velocity ratios (V_merid/V_merid@1st rotor LE) on the stream surface of the previous stage: {input_data['stages'][i-1]['meridional_velocity_ratios']}")
                    use_old_merid_vel_ratios = input('Use the meridional velocity ratios of the previous stage also in this stage [y/n]? ')
                    match use_old_merid_vel_ratios.lower():
                        case 'y':
                            meridional_velocity_ratios = input_data['stages'][i-1]['meridional_velocity_ratios'].copy()
                        case 'n':
                            # returns a string '0.5 0.6 07' => split at spaces...
                            meridional_velocity_ratios = input('Meridional velocity ratios (V_merid/V_merid@1st rotor LE) on the stream surface (space-separated): ').split()
                            # ... and turn each piece in a float
                            meridional_velocity_ratios = list(map(float, meridional_velocity_ratios))
                        case _:
                            raise ValueError(f"Unknown answer '{use_old_merid_vel_ratios}'")
                    stage_data['meridional_velocity_ratios'] = meridional_velocity_ratios.copy()
                    
                if i > 0:
                    print('"Indices of the leading and trailing edge of the previous stage (starting from index 1 on the mean stream surface): \n'
                          "\t Leading edge blade 1: point {input_data['stages'][i-1]['LE_TE_mean_stream_surf'][0]]}"
                          "\t Trailing edge blade 1: point {input_data['stages'][i-1]['LE_TE_mean_stream_surf'][1]]}"
                          "\t Leading edge blade 2: point {input_data['stages'][i-1]['LE_TE_mean_stream_surf'][2]]}"
                          "\t Trailing edge blade 2: point {input_data['stages'][i-1]['LE_TE_mean_stream_surf'][3]]}")
                    
                    use_old_LE_TE_idx = input('Use the leading and trailing edge indices of the previous stage also in this stage [y/n]? ')
                    match use_old_LE_TE_idx.lower():
                        case 'y':
                            idx_LE_TE_mean_stream = input_data['stages'][i-1]['idx_LE_TE_mean_stream'].copy()
                        case 'n':
                            # returns a string '0.5 0.6 07' => split at spaces...
                            idx_LE_TE_mean_stream = input('Leading and trailing edge indices on the stream surface (4 values, space-separated): ').split()
                            # ... and turn each piece in a float
                            idx_LE_TE_mean_stream = list(map(float, idx_LE_TE_mean_stream))
                        case _:
                            raise ValueError(f"Unknown answer '{use_old_LE_TE_idx}'")
                if len(idx_LE_TE_mean_stream) != 4:
                    raise ValueError('You must input 4 values: LE blade 1, TE blade 1, LE blade 2, TE blade 2')
                stage_data['LE_TE_mean_stream_surf'] = idx_LE_TE_mean_stream.copy()
                
                # MESH RECAP
                # for the table only: list of empty strings with 4 labels
                LE_TE_stream = ['']*N_pts_stream_surf
                LE_TE_stream[idx_LE_TE_mean_stream[0]] = 'LE 1'
                LE_TE_stream[idx_LE_TE_mean_stream[1]] = 'TE 1'
                LE_TE_stream[idx_LE_TE_mean_stream[2]] = 'LE 2'
                LE_TE_stream[idx_LE_TE_mean_stream[3]] = 'TE 2'
                mesh_recap = PrettyTable()
                mesh_recap.title = 'Stream surface coordinates - Stage {i}'
                mesh_recap.add_column('Axial [m]', axial_stream_coords)
                mesh_recap.add_column('Radial [m]', radial_stream_coords)
                mesh_recap.add_column('V_m/V_m@LE rotor 1 [-]', meridional_velocity_ratios)
                mesh_recap.add_column('LE/TE?', LE_TE_stream)
                
                if change_flow_stage and flow_new == 'mixed':
                    print("Moving the last stream surface point to the trailing edge of blade 2 (required when machine flow type is changed from 'mixed' to 'axial'...")
                    # (-1 because Fortran is 1-based indexing, but Python is 0-based)
                    axial_stream_coords_out = axial_stream_coords[idx_LE_TE_mean_stream-1]
                
                change_stream_surf_coords = input('Change the new stream surface coordinates [y/n]?')
                match change_stream_surf_coords.lower():
                    case 'y':
                        change_stream_surf_coords = True
                    case 'n':
                        change_stream_surf_coords = False
                    case _:
                        raise ValueError(f"Unknown answer '{change_stream_surf_coords}'")
                stage_data['change_stream_surf_coords'] = change_stream_surf_coords
        elif change_flow_stage and stage_flow_type == 'axial':
            aux.print_message('For an axial stage, there are 3 possible set of inputs you can use to specify the velocity triangles: '
                              '\n\t A) reaction degree, flow coefficient and stage loading coefficient'
                              '\n\t B) flow coefficient, stator exit angle and rotor exit angle'
                              '\n\t C) flow coefficient, rotor inlet angle and rotor exit angle'
                              '\n\t D) reaction degree, first blade row inlet angle and first blade row exit angle', 
                              aux.MessageLevel.INFO)
            input_method = input('Choose an input method [a/b/c/d]: ')
            match input_method.lower():
                case 'a':
                    input_method = 'chi_phi_psi'
                case 'b':
                    input_method = 'phi_statout_rotout'
                case 'c':
                    input_method = 'phi_rotin_rotout'
                case 'd':
                    input_method = 'chi_rowin_rowout'
                case _:
                    raise ValueError("Unknown input method '{input_method}'")
            stage_data['velocity_triangles_method'] = input_method
            
            match input_method:
                case 'chi_phi_psi':
                    chi = float(input('Reaction degree: '))
                    if chi < 0 or chi > 1:
                        aux.print_message('While technically not impossible, depending on the definition, having a rection degree < 0 or > 1 is probably wrong...', aux.MessageLevel.WARNING)
                    stage_data['reaction_degree'] = chi
                    
                    phi = float(input('Flow coefficient: '))
                    if phi < 0:
                        raise ValueError('Flow coefficient cannot be zero or negative')
                    stage_data['flow_coeff'] = phi
                    
                    psi = float(input('Stage loading coefficient: '))
                    if psi < 0:
                        raise ValueError('Stage loading coefficient cannot be zero or negative')
                    stage_data['stage_load_coeff'] = psi
                case 'phi_statout_rotout':
                    phi = float(input('Flow coefficient: '))
                    if phi < 0:
                        raise ValueError('Flow coefficient cannot be zero or negative')
                    stage_data['flow_coeff'] = phi
                    
                    # TODO: non ho capito se siano angoli assoluti o relativi
                    # per il rotore...
                    angle_stat_out = float(input('Stator exit angle [deg]: '))
                    if abs(angle_stat_out) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_stat_out'] = angle_stat_out
                    
                    angle_rot_out = float(input('Rotor exit angle [deg]: '))
                    if abs(angle_rot_out) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_rot_out'] = angle_rot_out
                case 'phi_rotin_rotout':
                    phi = float(input('Flow coefficient: '))
                    if phi < 0:
                        raise ValueError('Flow coefficient cannot be zero or negative')
                    stage_data['flow_coeff'] = phi
                    
                    # TODO: non ho capito se siano angoli assoluti o relativi
                    # per il rotore...
                    angle_rot_in = float(input('Rotor inlet angle [deg]: '))
                    if abs(angle_rot_in) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_rot_in'] = angle_rot_in
                    
                    angle_rot_out = float(input('Rotor exit angle [deg]: '))
                    if abs(angle_rot_out) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_rot_out'] = angle_rot_out
                case 'chi_rowin_rowout':
                    chi = float(input('Reaction degree: '))
                    if chi < 0 or chi > 1:
                        aux.print_message('While technically not impossible, depending on the definition, having a rection degree < 0 or > 1 is probably wrong...', aux.MessageLevel.WARNING)
                    stage_data['reaction_degree'] = chi
                    
                    angle_row_in = float(input('First blade row inlet angle [deg]: '))
                    if abs(angle_row_in) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_row_in'] = angle_row_in
                    
                    angle_row_out = float(input('First blade row exit angle [deg]: '))
                    if abs(angle_row_out) > 90:
                        raise ValueError('All angles must lie in the range [-90, +90] deg')
                    stage_data['angle_row_out'] = angle_row_out
            
            aux.print_message('For an axial stage, there are 2 ways to set the design radius:'
                  '\n\t A) input the design radius directly'
                  '\n\t B) input the stage enthalpy change', 
                              aux.MessageLevel.INFO)
            design_radius_method = input('Method to set the design radius [a/b]: ')
            match design_radius_method.lower():
                case 'a':
                    design_radius_method = 'set_radius'
                case 'b':
                    design_radius_method = 'set_enthalpy_change'
                case _:
                    raise ValueError(f"Unknown method '{design_radius_method}'")
            stage_data['design_radius_method'] = design_radius_method
            
            match design_radius_method:
                case 'set_radius':
                    R_design = float(input('Design point radius [m]: '))
                    if R_design <= 0:
                        raise ValueError('A radius cannot be zero or negative')
                    stage_data['design_radius'] = R_design
                case 'set_enthalpy_change':
                    dh_stage = float(input('Stage actual enthalpy change (absolute value) [kJ/kg]: '))
                    # TODO: il caso con dh = 0 va escluso o considerato?
                    if dh_stage < 0:
                        raise ValueError('The stage actual enthalpy change must be provided in modulus, no matter if it is an increase or a decrease in enthalpy')
                    # [kJ/kg] -> [J/kg]
                    stage_data['actual_enthalpy_change'] = 1e3 * dh_stage
            
            # TODO: non so dove vadano questi! sono solo per il caso assiale??
            aux.print_message('Default axial blade chords:'
                              f'\n\t Row 1: {meangen_def.c_ax_1}'
                              f'\n\t Row 2: {meangen_def.c_ax_2}',
                              aux.MessageLevel.INFO)
            change_c_ax = input('Change the axial blade chords default values [y/n]? ')
            match change_c_ax.lower():
                case 'y':
                    change_c_ax = True
                case 'n':
                    change_c_ax = False
                case _:
                    raise ValueError(f"Unknown answer '{change_c_ax}'")
            
            if change_c_ax:
                c_ax_1 = float(input('First blade row axial chord [m]: '))
                if c_ax_1 <= 0:
                    # actually, it could be zero, but then the blade is blocking the meridional channel
                    raise ValueError('An (axial) blade chord cannot be zero or negative')
                stage_data['axial_chord_1'] = c_ax_1
                
                c_ax_2 = float(input('Second blade row axial chord [m]: '))
                if c_ax_2 <= 0:
                    # actually, it could be zero, but then the blade is blocking the meridional channel
                    raise ValueError('An (axial) blade chord cannot be zero or negative')
                stage_data['axial_chord_2'] = c_ax_2
            else:
                stage_data['axial_chord_1'] = meangen_def.c_ax_1
                stage_data['axial_chord_2'] = meangen_def.c_ax_2
            
            aux.print_message('Default inter-row gap and inter-stage gap as fractions of the first row axial chord (gap/c_ax_1):'
                              f'\n\t Inter-row gap/axial_chord_1: {meangen_def.row_gap2cax}'
                              f'\n\t Inter-stage gap/axial_chord_1: {meangen_def.stage_gap2cax}',
                              aux.MessageLevel.INFO)
            change_axial_gaps = input('Change the inter-row and inter-stage axial gaps default values [y/n]? ')
            match change_axial_gaps.lower():
                case 'y':
                    change_axial_gaps = True
                case 'n':
                    change_axial_gaps = False
                case _:
                    raise ValueError(f"Unknown answer '{change_axial_gaps}'")

            if change_axial_gaps:
                row_gap = float(input('Inter-row gap/axial_chord_1: '))
                if row_gap <= 0:
                    # it could be zero in a simplified model (?)
                    raise ValueError('The non-dimensional inter-row gap cannot be zero or negative')
                stage_data['row_gap2cax'] = row_gap
                
                stage_gap = float(input('Inter-stage gap/axial_chord_1: '))
                if stage_gap <= 0:
                    # it could be zero in a simplified model (?)
                    raise ValueError('The non-dimensional inter-stage gap cannot be zero or negative')
                stage_data['stage_gap2cax'] = stage_gap
            else:
                stage_data['row_gap2cax'] = meangen_def.row_gap2cax
                stage_data['stage_gap2cax'] = meangen_def.stage_gap2cax
            
        
        # ---------- DATA FOR BOTH AXIAL AND MIXED FLOW TYPE ----------
        aux.print_message('NB: blockage factor = sum of the hub and casing boundary layer displacement thicknesses, divided by the blade span',
                          aux.MessageLevel.INFO)
        aux.print_message('Default values: \n'
              f'\t BL at LE of 1st row: {meangen_def.blockageLE_1} \n'
              f'\t BL at TE of 2nd row: {meangen_def.blockageTE_2}',
                          aux.MessageLevel.INFO)
        
        change_BF = input('Change the blockage factor default values [y/n]? ')
        match change_stream_surf_coords.lower():
            case 'y':
                change_stream_surf_coords = True
            case 'n':
                change_stream_surf_coords = False
            case _:
                raise ValueError(f"Unknown answer '{change_stream_surf_coords}'")
        stage_data['change_stream_surf_coords'] = change_stream_surf_coords
        
        if change_BF:
            BF_LE = float(input('Blockage factor at the leading edge of the 1st blade row: '))
            if BF_LE <= 0:
                raise ValueError('The blockage factor cannot be zero or negative')
            stage_data['blockage_factor_LE_first'] = BF_LE
            
            BF_TE = float(input('Blockage factor at the trailing edge of the 1st blade row: '))
            if BF_LE <= 0:
                raise ValueError('The blockage factor cannot be zero or negative')
            stage_data['blockage_factor_TE_last'] = BF_TE
        else:
            # copy default values
            stage_data['blockage_factor_LE_first'] = meangen_def.blockageLE_1
            stage_data['blockage_factor_TE_last'] = meangen_def.blockageTE_2
        
            
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