#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEANGEN auxiliary functions, mainly for I/O.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import yaml
from pathlib import Path
from textwrap import dedent
from shutil import copy2
from prettytable import PrettyTable


def create_meangen_input_file(yaml_file, meangen_file='meangen.in', out_dir=None):
    """
    Read YAML input file, echo input to the screen, check it and create a
    MEANGEN input file.

    Parameters
    ----------
    yaml_file : str or Path
        YAML input file path.
    meangen_file : str or Path, optional
        MEANGEN input file name. The default is 'meangen.in'.
    out_dir : str or Path, optional
        Path of the directory where the MEANGEN input file is be saved. 
        If None, it defaults to the parent directory of the YAML input file.
        The default is None.

    Raises
    ------
    ValueError
        If any input parameter has an invalid value.

    Returns
    -------
    input_data : dict
        Content of the YAML input file.

    """
    
    # format: <input_data_name> : <value>
    line_format = "\t{:40s} : {} {}"
    
    # convert to Paht object (if not already one)
    yaml_file = Path(yaml_file)
    # .resolve() to get absolute path with original upper/lower-case
    print(f'Reading YAML input file \n\t{yaml_file.resolve()}')
    with open(yaml_file, 'r') as file:
        input_data = yaml.safe_load(file)
    
    
    # ----------------------------- MACHINE DATA -----------------------------
    # convert data from YAML to MEANGEN original format + check inputs
    print('MACHINE DATA')
    meangen_input = []
    match input_data['machine']:
        case 'compressor':
            machine = 'C'
        case 'turbine':
            machine = 'T'
        case _:
            raise ValueError(f"Invalid machine option '{input_data['machine']}'")
    _add_block(meangen_input, rf"""
              {machine}                        TURBO_TYP,"C" FOR A COMPRESSOR,"T" FOR A TURBINE""")
    print(line_format.format('Machine', input_data['machine'], ''))
    
    match input_data['machine_flow_type']:
        case 'mixed':
            machine_type = 'MIX'
        case _:
            raise ValueError(f"Invalid machine flow type '{input_data['machine_flow_type']}'")
    _add_block(meangen_input, rf"""
              {machine_type}                      FLO_TYP FOR AXIAL OR MIXED FLOW MACHINE""")
    print(line_format.format('Machine flow type', input_data['machine_flow_type'], ''))
    
    if input_data['gas_properties']['gas_constant'] < 0:
        raise ValueError('Gas constant cannot be negative')
    if input_data['gas_properties']['gamma'] < 0:
        raise ValueError('Gamma cannot be negative')
    _add_block(meangen_input, rf"""
              {input_data['gas_properties']['gas_constant']}     {input_data['gas_properties']['gamma']}     GAS PROPERTIES, RGAS, GAMMA""")
    print(line_format.format('Gas constant', input_data['gas_properties']['gas_constant'], 'J/kgK'))
    print(line_format.format('Gamma Cp/Cv', input_data['gas_properties']['gamma'], ''))
    
    if input_data['inlet_conditions']['total_pressure'] < 0:
        raise ValueError('Total inlet pressure cannot be negative')
    if input_data['inlet_conditions']['total_temperature'] < 0:
        raise ValueError('Total inlet temperature cannot be negative')
    _add_block(meangen_input, rf"""
              {input_data['inlet_conditions']['total_pressure']}     {input_data['inlet_conditions']['total_temperature']}     POIN,  TOIN""")
    print(line_format.format('Total inlet pressure', input_data['inlet_conditions']['total_pressure'], 'bar'))
    print(line_format.format('Total inlet temperature', input_data['inlet_conditions']['total_temperature'], 'K'))
    
    if not isinstance(input_data['N_stages'], int):
        raise ValueError('Number of stages must be an integer')
    _add_block(meangen_input, rf"""
              {input_data['N_stages']}                    NUMBER OF STAGES IN THE MACHINE """)
    print(line_format.format('Number of stages', input_data['N_stages'], ''))
    
    match input_data['design_point_radius']:
        case 'hub':
            design_radius = 'H'
        case 'mid':
            design_radius = 'M'
        case 'tip':
            design_radius = 'T'
        case _:
            raise ValueError(f"Invalid design point radius '{input_data['design_point_radius']}'")
    _add_block(meangen_input, rf"""
              {design_radius}                        CHOICE OF DESIGN POINT RADIUS, HUB, MID or TIP""")
    print(line_format.format('Design point radius', input_data['design_point_radius'], ''))
    
    if input_data['rotation_speed'] < 0:
        raise ValueError('Rotation speed cannot be negative')
    _add_block(meangen_input, rf"""
              {input_data['rotation_speed']}             ROTATION SPEED, RPM""")
    print(line_format.format('Rotation speed', input_data['rotation_speed'], 'rpm'))
    
    if input_data['mass_flow_rate'] < 0:
        raise ValueError('Mass flow rate cannot be negative')
    _add_block(meangen_input, rf"""
              {input_data['mass_flow_rate']}             MASS FLOW RATE, FLOWIN.""")
    print(line_format.format('Mass flow rate', input_data['mass_flow_rate'], 'kg/s'))
    
    # TODO
    #     B                        MIXTYP = INPUT TYPE FOR FLO_TYP = "MIX" .
    
    if input_data['phi_first_rotor_LE'] < 0:
        raise ValueError('Flow coefficient at the first rotor leading edge cannot be negative')
    _add_block(meangen_input, rf"""
              {input_data['phi_first_rotor_LE']}               FLOW COEFFICIENT AT THE FIRST ROTOR LEADING EDGE.""")
    print(line_format.format('Flow coefficient at 1st rotor LE', input_data['phi_first_rotor_LE'], ''))
    
    
    # ------------------------------ STAGE DATA ------------------------------
    use_last_stage_rotor = []
    use_last_stage_stator = []
    for stage_idx in input_data['stages']:
        print(f'STAGE {stage_idx} DATA')
        stage = input_data['stages'][stage_idx].copy()
        
        if abs(stage['alpha_in']) > 90:
            raise ValueError('Stage inlet absolute flow angle cannot be >90° or <-90°')
        if abs(stage['alpha_out']) > 90:
            raise ValueError('Stage outlet absolute flow angle cannot be >90° or <-90°')
        _add_block(meangen_input, rf"""
                  {stage['alpha_in']}     {stage['alpha_out']}     STAGE INLET AND OUTLET ABSOLUTE FLOW ANGLES.""")
        print(line_format.format('Inlet absolute flow angle', stage['alpha_in'], 'deg'))
        print(line_format.format('Outlet absolute flow angle', stage['alpha_out'], 'deg'))
        
        if stage['psi_rotor_LE'] < 0:
            raise ValueError('Stage loading coefficient at the rotor leading edge cannot be negative')
        _add_block(meangen_input, rf"""
                  {stage['psi_rotor_LE']}               STAGE LOADING COEFFICIENT AT THE ROTOR LEADING EDGE.""")
        print(line_format.format('Stage loading coefficient at rotor LE', stage['psi_rotor_LE'], ''))
        
        if stage['N_points_stream_surface'] < 0:
            raise ValueError('Number of points on the stream surface cannot be negative')
        _add_block(meangen_input, rf"""
                  {stage['N_points_stream_surface']}                    NUMBER OF POINTS ON THE STREAM SURFACE.""")
        print(line_format.format('Number of points on the stream surface', stage['N_points_stream_surface'], ''))
        
        if len(stage['stream_surf_axial_coords']) != stage['N_points_stream_surface']:
            raise ValueError(f"The number of stream surface axial coordinates must match the given number of points on the stream surface ({stage['N_points_stream_surface']})")
        
        if len(stage['stream_surf_radial_coords']) != stage['N_points_stream_surface']:
            raise ValueError(f"The number of stream surface radial coordinates must match the given number of points on the stream surface ({stage['N_points_stream_surface']})")
        
        if len(stage['meridional_velocity_ratios']) != stage['N_points_stream_surface']:
            raise ValueError(f"The number of meridional axial velocity ratios must match the given number of points on the stream surface ({stage['N_points_stream_surface']})")
        
        stream_surf = PrettyTable()
        stream_surf.title = 'Stream surface'
        stream_surf.add_column('Axial coordinates [m]', stage['stream_surf_axial_coords'])
        stream_surf.add_column('Radial coordinates [m]', stage['stream_surf_radial_coords'])
        stream_surf.add_column('Meridional velocity ratio [-]', stage['meridional_velocity_ratios'])
        print(stream_surf)
        
        # TODO
        #         2    3    4    5     LEADING AND TRAILING EDGE POINTS ON THE MEAN STREAM SURFACE.
        
        if not isinstance(stage['change_stream_surf_coords'], bool):
            raise ValueError('Use a boolean to select whether to change the stream surface coordinates!')
        if stage['change_stream_surf_coords']:
            change_stream_surf_coords = 'Y'
        else:
            change_stream_surf_coords = 'N'
        _add_block(meangen_input, rf"""
                  {change_stream_surf_coords}                        DO YOU WANT TO CHANGE THE STREAM SURFACE COORDINATES ?""")
        print(line_format.format('Change stream surface coordinates?', stage['change_stream_surf_coords'], ''))
        
        if stage['blockage_LE'] < 0:
            raise ValueError('Leading edge blockage factor cannot be negative')
        if stage['blockage_TE'] < 0:
            raise ValueError('Trailing edge blockage factor cannot be negative')
        _add_block(meangen_input, rf"""
                  {stage['blockage_LE']}   {stage['blockage_TE']}     BLOCKAGE FACTORS, FBLOCK_LE,  FBLOCK_TE .""")
        print(line_format.format('LE blockage factor', stage['blockage_LE'], ''))
        print(line_format.format('TE blockage factor', stage['blockage_TE'], ''))
        
        if stage['eta_iso_stage_guess'] < 0 or stage['eta_iso_stage_guess'] > 1:
            raise ValueError('Guessed stage isentropic efficiency must be in between 0 and 1')
        _add_block(meangen_input, rf"""
                  {stage['eta_iso_stage_guess']}             GUESS OF THE STAGE ISENTROPIC EFFICIENCY""")
        print(line_format.format('Guessed stage isentropic efficiency', stage['eta_iso_stage_guess'], ''))
        
        if abs(stage['delta_first_row']) > 90:
            raise ValueError('Estimated first row deviation angle cannot be >90° or <-90°')
        if abs(stage['delta_second_row']) > 90:
            raise ValueError('Estimated second row deviation angle cannot be >90° or <-90°')
        _add_block(meangen_input, rf"""
                  {stage['delta_first_row']}   {stage['delta_second_row']}         ESTIMATE OF THE FIRST AND SECOND ROW DEVIATION ANGLES""")
        print(line_format.format('Estimated 1st row deviation angle', stage['delta_first_row'], 'deg'))
        print(line_format.format('Estimated 2nd row deviation angle', stage['delta_second_row'], 'deg'))
        
        if abs(stage['incidence_first_row']) > 90:
            raise ValueError('First row incidence angle cannot be >90° or <-90°')
        if abs(stage['incidence_second_row']) > 90:
            raise ValueError('Second row incidence angle cannot be >90° or <-90°')
        _add_block(meangen_input, rf"""
                   {stage['incidence_first_row']}  {stage['incidence_second_row']}         FIRST AND SECOND ROW INCIDENCE ANGLES""")
        print(line_format.format('1st row incidence angle', stage['incidence_first_row'], 'deg'))
        print(line_format.format('2nd row incidence angle', stage['incidence_second_row'], 'deg'))
        
        # TODO
        #        1.00000               BLADE TWIST OPTION, FRAC_TWIST
        #     n                        BLADE ROTATION OPTION , Y or N
        #       88.000  92.000         QO ANGLES AT LE  AND TE OF ROW 1 
        #       92.000  88.000         QO ANGLES AT LE  AND TE OF ROW 2 
        
        
        if not isinstance(stage['change_stage_angles'], bool):
            raise ValueError('Use a boolean to select whether to change the angles of this stage!')
        if stage['change_stage_angles']:
            change_stage_angles = 'Y'
        else:
            change_stage_angles = 'N'
        _add_block(meangen_input, rf"""
                  {change_stage_angles}                        DO YOU WANT TO CHANGE THE ANGLES FOR THIS STAGE ? "Y" or "N" """)
        print(line_format.format('Change the angles for this stage?', stage['change_stage_angles'], ''))
        
        # TODO
        #     n                        IFSAME_ALL, SET = "Y" TO REPEAT THE LAST STAGE INPUT TYPE AND VELOCITY TRIANGLES, SET = "C" TO CHANGE INPUT TYPE.
        
        
        # these options belong LOGICALLY to this point, but they're listed at
        # the bottom of the file, so they're printed to file later in the code
        if not isinstance(stage['use_last_stage_blade_section']['rotor'], bool):
            raise ValueError('Use a boolean to select whether to use the same blade section as the last stage for the rotor!')
        if stage['use_last_stage_blade_section']['rotor']:
            use_last_stage_rotor.append('Y')
        else:
            use_last_stage_rotor.append('N')
        print(line_format.format('Use last stage blade sections (rotor)?', stage['use_last_stage_blade_section']['rotor'], ''))
        
        if not isinstance(stage['use_last_stage_blade_section']['stator'], bool):
            raise ValueError('Use a boolean to select whether to use the same blade section as the last stage for the stator!')
        if stage['use_last_stage_blade_section']['stator']:
            use_last_stage_stator.append('Y')
        else:
            use_last_stage_stator.append('N')
        print(line_format.format('Use last stage blade sections (stator)?', stage['use_last_stage_blade_section']['stator'], ''))
        
        
    # -------------------------- GENERAL OPTIONS --------------------------
    print('GENERAL OPTIONS')
    if not isinstance(input_data['ouput_all_rows'], bool):
        raise ValueError('Use a boolean to select whether output is requested for all blade rows!')
    if input_data['ouput_all_rows']:
        ouput_all_rows = 'Y'
    else:
        ouput_all_rows = 'N'
    _add_block(meangen_input, rf"""
              {ouput_all_rows}                        IS OUTPUT REQUESTED FOR ALL BLADE ROWS ?""")
    print(line_format.format('Output all blade rows?', input_data['ouput_all_rows'], ''))
    
    
    # these lines logically belongs to another part of the screen output, but
    # they're printed at the bottom of the MEANGEN input file
    for stage_idx in input_data['stages']:
        # stages are numbered from 1 to N, not from 0 to N-1
        _add_block(meangen_input, rf"""
                  {use_last_stage_rotor[stage_idx-1]}    ROTOR No.   {stage_idx} SET ANSTK = "Y" TO USE THE SAME  BLADE SECTIONS AS THE LAST STAGE""")
        _add_block(meangen_input, rf"""
                  {use_last_stage_stator[stage_idx-1]}    STATOR No.   {stage_idx} SET ANSTK = "Y" TO USE THE SAME  BLADE SECTIONS AS THE LAST STAGE""")
    
    
    # print to file
    # if not given, save the MEANGEN input file in the yaml file directory
    if out_dir is None:
        # use .resolve() to have it "clean" and substitue all the . and .. with
        # directories' names
        out_dir = yaml_file.parent.resolve()
    else:
        out_dir = Path(out_dir)
    meangen_file = out_dir / meangen_file
    print(f'Writing input in a MEANGEN-compatible format to \n\t{meangen_file.resolve()}')
    with open(meangen_file, 'w') as file:
        # concatenate lines to a single string, separating them with newlines
        file.writelines('\n'.join(meangen_input))
    
    
    return input_data


def create_fresh_input_file(case_dir, input_file=None):
    """
    Create a clean YAML input file.

    Parameters
    ----------
    case_dir : Path or str
        Directory where the new input file is copied into.
    input_file : Path or str, optional
        Name of the YAML input file. If None, the original name 'input.yaml' is
        used. The default is None.

    Returns
    -------
    None.

    """
    
    case_dir = Path(case_dir)
    print(f'Creating clean YAML input file in \n\t{case_dir.resolve()}')
    # copy input.yaml file into the given directory
    # (since a directory is given as destination, the original filename is kept)
    copy2(Path('./input.yaml'), case_dir)
    

# -----------------------------------------------------------------------------
#                           PRIVATE FUNCTIONS
# -----------------------------------------------------------------------------

def _add_block(code, new_block):
    # remove indentation, if present
    new_code = dedent(new_block)
    # remove leading and trailing whitespaces, if any
    new_code = new_code.strip()
    # and return a list of strings, one per line
    new_code = new_code.splitlines()
    # now append it to the original list
    # (using .append() would create a list with another list inside it, like
    # [1, 3, [5, 6]], rather than a single list like [1, 3, 5, 6])
    code.extend(new_code)
    return code
    

if __name__ == '__main__':
    yaml_file = Path('../../prova/2stg-compr-meangen-17.4.yaml')
    #yaml_file = Path('../../prova/prova.yaml')
    input_data = create_meangen_input_file(yaml_file)
    create_fresh_input_file('../../prova')