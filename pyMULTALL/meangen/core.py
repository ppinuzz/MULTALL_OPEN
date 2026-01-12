#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEANGEN core functions.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

import subprocess
from dataclasses import dataclass

import pyMULTALL.meangen as meangen
import pyMULTALL.auxiliaries as aux

@dataclass
class MeangenOptions:
    # whether to use Denton's original Fortran compiled executable MEANGEN.exe
    Fortran: bool = True


def MEANGEN(case_dir, opts=MeangenOptions()):
    
    if opts.Fortran:
        print("Running Denton's original MEANGEN Fortran executable...")
        MEANGEN_EXE = meangen.defaults.MEANGEN
        
        # check if file exists
        # https://stackoverflow.com/a/82852/17220538
        if not MEANGEN_EXE.is_file():
            raise FileNotFoundError(f'MEANGEN executable {meangen.defaults.MEANGEN.resolve()} does NOT exists')
        else:
            print(f'MEANGEN executable: \n\t{meangen.defaults.MEANGEN.resolve()}')


        if aux.get_OS_name() == aux.OperatingSystem.WINDOWS:
            subprocess.Popen(
                # run MEANGEN executable through Windows' CMD, keeping the terminal 
                # window open (/k) after MEANGEN has terminated the execution
                ['cmd.exe', '/k', str(MEANGEN_EXE.resolve())],
                # ensure a new console window is opened
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                # start MEANGEN in the case directory where the meangen.in input file
                # (required by MEANGEN)
                cwd=case_dir.resolve()
            )
        
    else:
        raise NotImplementedError('Python version of MEANGEN is not implemented yet')
    