#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Default values for several MEANGEN parameters.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

from dataclasses import dataclass
from pathlib import Path
from pyMULTALL.defaults import PYMULTALL

# path of MEANGEN executable w.r.t. this file
MEANGEN = PYMULTALL / 'bin'/ 'MEANGEN.exe'

@dataclass 
class TurbineOpts:
    # leading edge thickness / axial chord
    tLE2cax: float = 0.04
    # trailing edge thickness / axial chord
    tTE2cax: float = 0.04
    # stator max thickness / axial chord
    tmax_stat2cax: float = 0.30
    # rotor max thickness / axial chord
    tmax_rot2cax: float = 0.25
    # position of the stator maximum thickness section as a fraction of the axial chord
    pos_tmax_stat2cax: float = 0.45
    # position of the rotor maximum thickness section as a fraction of the axial chord
    pos_tmax_rot2cax: float = 0.40
    # "fraction of axial chord over which the leading edge is modified"
    pos_modLE2cax: float = 0.02
    # "fraction of axial chord over which the trailing edge is modified"
    pos_modTE2cax: float = 0.01
    # Zweifel coefficient
    Zw: float = 0.85
    # "EXPONENT FOR TRANSFORMING THE AXIAL POSITION. IT IS USED TO VARY THE CAMBER 
    #LINE SHAPE. INCREASING EXPO MOVES THE BLADE LOADING UPSTREAM."
    exp: float = 1.0
    # angle between leading edge and axial direction in meridional view
    thetaLE2ax_merid_1: float = 92.0     # row 1
    thetaLE2ax_merid_2: float = 88.0     # row 2
    # angle between trailing edge and axial direction in meridional view
    thetaTE2ax_merid_1: float = 88.0     # row 1
    thetaTE2ax_merid_2: float = 92.0     # row 2
    # "FORM OF BLADE THICKNESS DISTRIBUTION
    thickness_distribution:int = 2

# =============================================================================
#   IF(TURBO_TYP.EQ.'T') THEN   !   DEFAULTS FOR TURBINES.
#        TKLE     = 0.04 ! LEADING EDGE THICKNESS/AXIAL CHORD.
#        TKTE     = 0.04 ! TRAILING EDGE THICKNESS/AXIAL CHORD.
#        TKMAXS   = 0.30 ! STATOR MAXIMUM THICKNESS/AXIAL CHORD.
#        TKMAXR   = 0.25 ! ROTOR MAXIMUM THICKNESS/AXIAL CHORD.
#        XTKMAXS  = 0.45 ! FRACTION OF AXIAL CHORD AT MAXIMUM THICKNESS FOR STATOR
#        XTKMAXR  = 0.40 ! FRACTION OF AXIAL CHORD AT MAXIMUM THICKNESS FOR ROTOR
#        XMODLE   = 0.02 ! FRACTION OF AXIAL CHORD OVER WHICH THE LE IS MODIFIED.
#        XMODTE   = 0.01 ! FRACTION OF AXIAL CHORD OVER WHICH THE TE IS MODIFIED.
#        TK_TYP   = 2.0  ! FORM OF BLADE THICKNESS DISTRIBUTION.
#        ZWEIFEL  = 0.85 ! ZWEIFEL COEFFICIENT FOR TURBINES
#        EXPO     = 1.0  ! EXPONENT FOR TRANSFORMING THE AXIAL POSITION. IT IS USED TO
# C                            VARY THE CAMBER LINE SHAPE. INCREASING EXPO MOVES THE BLADE LOADING UPSTREAM.
#        QLE_ROW1(1) = 92.0  ! LEADING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 1.
#        QTE_ROW1(1) = 88.0  ! TRAILING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 1.
#        QLE_ROW2(1) = 88.0  ! LEADING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 2.
#        QTE_ROW2(1) = 92.0  ! TRAILING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 2.
#   END IF
# =============================================================================

@dataclass
class CompressorOpts:
    # leading edge thickness / axial chord
    tLE2cax: float = 0.02
    # trailing edge thickness / axial chord
    tTE2cax: float = 0.01
    # stator max thickness / axial chord
    tmax_stat2cax: float = 0.10
    # rotor max thickness / axial chord
    tmax_rot2cax: float = 0.075
    # position of the stator maximum thickness section as a fraction of the axial chord
    pos_tmax_stat2cax: float = 0.45
    # position of the rotor maximum thickness section as a fraction of the axial chord
    pos_tmax_rot2cax: float = 0.40
    # TODO: unclear
    # "fraction of axial chord over which the leading edge is modified"
    pos_modLE2cax: float = 0.02
    # TODO: unclear
    # "fraction of axial chord over which the trailing edge is modified"
    pos_modTE2cax: float = 0.01
    # "FORM OF BLADE THICKNESS DISTRIBUTION"
    # TODO: scoprire che thickness distribution corrisponde al 2
    thickness_distribution: int = 2
    # Zweifel coefficient
    Zw: float = 0.50
    # TODO: rimuovi se non serve?
    # "DIFFUSION FACTOR FOR COMPRESSORS. THIS IS NOT NOW USED."
    diffusion_factor: float = 0.35
    # TODO: unclear
    # "EXPONENT FOR TRANSFORMING THE AXIAL POSITION. IT IS USED TO VARY THE CAMBER 
    #LINE SHAPE. INCREASING EXPO MOVES THE BLADE LOADING UPSTREAM."
    exp: float = 1.0
    # TODO: sicuro di aver capito bene?
    # angle between leading edge and axial direction in meridional view
    thetaLE2ax_merid_1: float = 88.0     # row 1
    thetaLE2ax_merid_2: float = 92.0     # row 2
    # angle between trailing edge and axial direction in meridional view
    thetaTE2ax_merid_1: float = 92.0     # row 1
    thetaTE2ax_merid_2: float = 88.0     # row 2
    
    
# =============================================================================
#   IF(TURBO_TYP.EQ.'C') THEN   !  DEFAULTS FOR COMPRESSORS.
#        TKLE     = 0.02  ! LEADING EDGE THICKNESS/AXIAL CHORD. 
#        TKTE     = 0.01  ! TRAILING EDGE THICKNESS/AXIAL CHORD.
#        TKMAXS   = 0.10  ! STATOR MAXIMUM THICKNESS/AXIAL CHORD.
#        TKMAXR   = 0.075 ! ROTOR MAXIMUM THICKNESS/AXIAL CHORD.
#        XTKMAXS  = 0.45  ! FRACTION OF AXIAL CHORD AT MAXIMUM THICKNESS FOR STATOR
#        XTKMAXR  = 0.40  ! FRACTION OF AXIAL CHORD AT MAXIMUM THICKNESS FOR ROTOR
#        XMODLE   = 0.02  ! FRACTION OF AXIAL CHORD OVER WHICH THE LE IS MODIFIED.
#        XMODTE   = 0.01  ! FRACTION OF AXIAL CHORD OVER WHICH THE TE IS MODIFIED.
#        TK_TYP   = 2.0   ! DETERMINES THE SHAPE OF THE BLADE THICKNESS DISTRIBUTION.TYPICALLY = 2,
# C                             LARGER VALUES GIVE MORE UNIFORM THICKNESS.
#        ZWEIFEL  = 0.5   ! ZWEIFEL COEFFICIENT FOR COMPRESSORS.
#        D_FAC    = 0.35  ! DIFFUSION FACTOR FOR COMPRESSORS. THIS IS NOT NOW USED.
#        EXPO     = 1.35  ! EXPONENT FOR TRANSFORMING THE AXIAL POSITION. IT IS USED TO
# C                             VARY THE CAMBER LINE SHAPE. INCREASING EXPO MOVES THE BLADE LOADING UPSTREAM.
#        QLE_ROW1(1) = 88.0  ! LEADING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 1.
#        QTE_ROW1(1) = 92.0  ! TRAILING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 1.
#        QLE_ROW2(1) = 92.0  ! LEADING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 2.
#        QTE_ROW2(1) = 88.0  ! TRAILING EDGE ANGLE TO AXIAL DIRECTION IN MERIDINAL VIEW ROW 2.
#   END IF
# =============================================================================

# TODO: change this to a string
# use perfect gas properties
gas_props = 1
# gas constant [J/kgK] (default: air)
R_gas = 287.5 
# gas specific heat ratio Cp/Cv (default: air)
gamma_gas = 1.40

# axial chord [m]
c_ax_1 = 0.05   # row 1
c_ax_2 = 0.04   # row 2
# gap between blade rows / axial chord
row_gap2cax = 0.25
# gap between stages / axial chord
stage_gap2cax = 0.50
# deviation angle [deg]
delta_1 = 5.0   # row 1
delta_1 = 5.0   # row 2
# incidence angle [deg]
incidence_1 = -2.0   # row 1
incidence_2 = -2.0   # row 2
# isentropic efficiency
eta_iso = 0.90
# number of smoothing of the stream surface coordinates
N_smooth_stream = 5
# smoothing factor for stream surface smoothing
smoothing_factor = 0.1
# blockage factor at 1st leading edge
blockageLE_1 = 0.0
# blockage factor at 2nd blade trailing edge
blockageTE_2 = 0.0

# number of stream surfaces to be generated
N_stream_surfs = 3
# number of grid points in pitchwise direction
N_pts_pitch = 37
# number of grid points in spanwise direction
N_pts_span = 37
# number of meridional grid points upstream of the leading edge
N_pts_merid_LE = 20
# number of meridional grid points on the blade
N_pts_merid_blade = 70
# number of meridional grid points behind the trailing edge
N_pts_merid_TE = 15
# number of extra meridional points upstream of row 1
N_pts_extra_before = 5
# number of extra meridional points downstream of the last row
N_pts_extra_after = 5

# grid expansion ratio in pitchwise direction
exp_ratio_pitch = 1.25
# maximum grid expansion ratio in pitchwise direction
max_exp_ratio_pitch = 20.0
# grid expansion ratio in spanwise direction
exp_ratio_span = 1.25
# maximum grid expansion ratio in spanwise direction
max_exp_ratio_span = 20.0

# =============================================================================
# IPROPS     = 1       ! USE PERFECT GAS PROPERTIES. 
# RGAS       = 287.5   ! GAS CONSTANT, VALUE FOR AIR.
# GAMM       = 1.40    ! GAS SPECIFIC HEAT RATIO, VALUE FOR AIR.
# AXCHRD1(1) = 0.05    ! AXIAL CHORD OF ROW 1, METRES.
# AXCHRD2(1) = 0.04    ! AXIAL CHORD OF ROW 2, METRES. 
# ROWGAP(1)  = 0.25    ! GAP BETWEEN BLADE ROWS AS A FRACTION OF THE AXIAL CHORD.
# STAGEGAP(1)= 0.5     ! GAP BETWEEN STAGES AS A FRACTION OF THE AXIAL CHORD.
# DEVN_1     = 5.0     ! DEVIATION ANGLE FROM ROW 1, DEGREES.
# DEVN_2     = 5.0     ! DEVIATION ANGLE FRON ROW 2, DEGREES.
# AINC_1     = -2.0    ! INCIDENCE ANGLE ON ROW 1, DEGREES.
# AINC_2     = -2.0    ! INCIDENCE ANGLE ON ROW 2, DEGREES.
# ETA(1)     = 0.9     ! ISENTROPIC EFFICIENCY.
# NSMOOTH    = 5       ! NUMBER OF SMOOTHINGS OF THE STREAM SURFACE COORDINATES.
# SFAC       = 0.1     ! SMOOTHING FACTOR FOR THE STREAM SURFACE SMOOTHING.
# FBLOCK_LE(1) = 0.0   ! BLOCKAGE FACTOR AT FIRST LEADING EDGE.
# FBLOCK_TE(1) = 0.0   ! BLOCKAGE FACTOR AT SECOND BLADE TRAILING EDGE.
# 
# NOSECT  = 3    ! NUMBER OS STREAM SURFACES TO BE GENERATED.
# IM      = 37   ! NUMBER OF GRID POINTS IN THE PITCHWISE DIRECTION.
# KM      = 37   ! NUMBER OF GRID POINTS IN THE SPANWISE DIRECTION.
# NINTUP  = 20   ! NUMBER OF MERIDIONAL GRID POINTS UPSTREAM OF THE LEADING EDGE.
# NINTON  = 70   ! NUMBER OF MERIDIONAL GRID POINTS ON THE BLADE.
# NINTDWN = 15   ! NUMBER OF MERIDIONAL GRID POINTS BEHIND THE TRAILING EDGE.
# NADDUP  = 5    ! EXTRA MERIDIONAL GRID POINTS UPSTREAM OF ROW 1.
# NADDWN  = 5    ! EXTRA MERIIONAL GRID POINTS DOWNSTREAM OF THE LAST ROW.
# FPRAT   = 1.25 ! GRID EXPANSION RATIO IN THE PITCHWISE DIRECTION.
# FPMAX   = 20.0 ! MAXIMUM GRID EXPANSION IN THE PITCHWISE DIRECTION.
# FRRAT   = 1.25 ! GRID EXPANSION RATIO IN THE SPANWISE DIRECTION.
# FRMAX   = 20.0 ! MAXIMUM GRID EXPANSION IN THE SPANWISE DIRECTION.
# =============================================================================


