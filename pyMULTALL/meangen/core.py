#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEANGEN core functions.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import subprocess

import pyMULTALL.meangen as pymeangen
import pyMULTALL.auxiliaries as aux
from colorama import just_fix_windows_console
import yaml
from pathlib import Path
import sys

def meangen(case_dir, Fortran=True, input_file=None):
    
    # make ANSI colours work on Windows without installing anything else
    # (does nothing on other OSs)
    just_fix_windows_console()
    
    pymeangen.auxiliaries.print_startup_message()
    
    if Fortran:
        print("Running Denton's original MEANGEN Fortran executable...")
        MEANGEN_EXE = pymeangen.defaults.MEANGEN
        
        # check if file exists
        # https://stackoverflow.com/a/82852/17220538
        if not MEANGEN_EXE.is_file():
            raise FileNotFoundError(f'MEANGEN executable {pymeangen.defaults.MEANGEN.resolve()} does NOT exists')
        else:
            print(f'MEANGEN executable: \n\t{pymeangen.defaults.MEANGEN.resolve()}')


        if aux.get_OS_name() == aux.OperatingSystem.WINDOWS:
            meangen_process = subprocess.Popen(
                # run MEANGEN executable through Windows' CMD, keeping the terminal 
                # window open (/k) after MEANGEN has terminated the execution
                ['cmd.exe', '/k', str(MEANGEN_EXE.resolve())],
                # ensure a new console window is opened
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                # start MEANGEN in the case directory where the meangen.in input file
                # (required by MEANGEN)
                cwd=case_dir.resolve()
            )
            aux.print_message('Close MEANGEN terminal window to resume parent proces...', aux.MessageLevel.INFO)
            meangen_process.wait()
    else:
        input_file = Path(input_file)
        
        if '.yaml' not in input_file.stem:
            aux.print_message('Input file is not a .yaml file, but Python code can only take YAML as input. Aborting...', aux.MessageLevel.WARNING)
            raise SystemExit
        with open(input_file, 'r') as file:
            input_data = yaml.safe_load(file)
        
        raise NotImplementedError('Python version of MEANGEN is not implemented yet')

