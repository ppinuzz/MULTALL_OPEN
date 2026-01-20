#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Default values for several MEANGEN parameters.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

from dataclasses import dataclass
from pathlib import Path
from pyMULTALL.defaults import PYMULTALL
from pyMULTALL.auxiliaries import GasModel

# path of MEANGEN executable w.r.t. this file
MEANGEN = PYMULTALL / 'bin'/ 'MEANGEN.exe'
# last MEANGEN version as of 25/11/2025
VERSION = '17.4'

@dataclass
class StageOpts:
    """
    Default parameters and options for a machine stage, regardless of machine type.
    
    Parameters
    ----------
    c_ax_1 : float, optional
        Axial chord of the 1st row [m]. Default is 0.05 m.
    c_ax_2 : float, optional
        Axial chord of the 2nd row [m]. Default is 0.04 m.
    row_gap2cax : float, optional
        Gap between blade rows divided by axial chord: :math:`{{\Delta}} z_{rows}/c_{ax}`.
    stage_gap2cax : float, optional
        Gap between stages divided by axial chord: :math:`{{\Delta}} z_{stages}/c_{ax}`.
    delta_1 : float, optional
        Deviation angle of the 1st row (always > 0) [deg]. Default is 5.0 deg.
    delta_2 : float, optional
        Deviation angle of the 2nd row (always > 0) [deg]. Default is 5.0 deg.
    incidence_1 : float, optional
        Incidence angle of the 1st row [deg]. Default is -2.0 deg.
    incidence_2 : float, optional
        Incidence angle of the 2nd row [deg]. Default is -2.0 deg.
    eta_iso : float, optional
        Guessed stage isentropic efficiency. Default is 0.90.
    blockageLE_1 : float, optional
        Blockage factor at the 1st blade leading edge. Default is 0.0.
    blockageTE_2 : float, optional
        Blockage factor at the 2nd trailing edge. Default is 0.0.
    
    """
    # axial chord [m]
    c_ax_1: float = 0.05   # row 1
    c_ax_2: float = 0.04   # row 2
    # gap between blade rows / axial chord
    row_gap2cax: float = 0.25
    # gap between stages / axial chord
    stage_gap2cax: float = 0.50
    # deviation angle [deg]
    delta_1: float = 5.0   # row 1
    delta_2: float = 5.0   # row 2
    # incidence angle [deg]
    incidence_1: float = -2.0   # row 1
    incidence_2: float = -2.0   # row 2
    # isentropic efficiency
    eta_iso: float = 0.90
    # blockage factor at 1st leading edge
    blockageLE_1: float = 0.0
    # blockage factor at 2nd blade trailing edge
    blockageTE_2: float = 0.0


@dataclass
class NumericGridOpts:
    """
    Numerical grid options.

    Parameters
    ----------
    N_smooth_stream : int, optional
        Number of smoothing iterations applied to the stream surface
        coordinates. Default is 5.
    smoothing_factor : float, optional
        Relaxation factor used during stream surface smoothing.
        Default is 0.1.
    N_stream_surfs : int, optional
        Number of stream surfaces to be generated.
        Default is 3.
    N_pts_pitch : int, optional
        Number of grid points in the pitchwise direction.
        Default is 37.
    N_pts_span : int, optional
        Number of grid points in the spanwise direction.
        Default is 37.
    N_pts_merid_LE : int, optional
        Number of meridional grid points upstream of the leading edge.
        Default is 20.
    N_pts_merid_blade : int, optional
        Number of meridional grid points along the blade surface.
        Default is 70.
    N_pts_merid_TE : int, optional
        Number of meridional grid points downstream of the trailing edge.
        Default is 15.
    N_pts_extra_before : int, optional
        Number of additional meridional grid points upstream of the first row.
        Default is 5.
    N_pts_extra_after : int, optional
        Number of additional meridional grid points downstream of the last row.
        Default is 5.
    exp_ratio_pitch : float, optional
        Grid expansion ratio in the pitchwise direction.
        Default is 1.25.
    max_exp_ratio_pitch : float, optional
        Maximum allowed grid expansion ratio in the pitchwise direction.
        Default is 20.0.
    exp_ratio_span : float, optional
        Grid expansion ratio in the spanwise direction.
        Default is 1.25.
    max_exp_ratio_span : float, optional
        Maximum allowed grid expansion ratio in the spanwise direction.
        Default is 20.0.
    """
    # number of smoothing of the stream surface coordinates
    N_smooth_stream: int = 5
    # smoothing factor for stream surface smoothing
    smoothing_factor: float = 0.1
    # number of stream surfaces to be generated
    N_stream_surfs: int = 3
    # number of grid points in pitchwise direction
    N_pts_pitch: int = 37
    # number of grid points in spanwise direction
    N_pts_span: int = 37
    # number of meridional grid points upstream of the leading edge
    N_pts_merid_LE: int = 20
    # number of meridional grid points on the blade
    N_pts_merid_blade: int = 70
    # number of meridional grid points behind the trailing edge
    N_pts_merid_TE: int = 15
    # number of extra meridional points upstream of the first row
    N_pts_extra_before: int = 5
    # number of extra meridional points downstream of the last row
    N_pts_extra_after: int = 5
    # grid expansion ratio in pitchwise direction
    exp_ratio_pitch: float = 1.25
    # maximum grid expansion ratio in pitchwise direction
    max_exp_ratio_pitch: float = 20.0
    # grid expansion ratio in spanwise direction
    exp_ratio_span: float = 1.25
    # maximum grid expansion ratio in spanwise direction
    max_exp_ratio_span: float = 20.0


@dataclass 
class TurbineOpts(StageOpts):
    """
    Default parameters and options for a turbine stage.
    
    Parameters
    ----------
    tLE2cax : float, optional
        Leading-edge thickness divided by axial chord: :math:`t_{LE}/c_{ax}`.
        Default is 0.04.
    tTE2cax : float, optional
        Trailing-edge thickness divided by axial chord: :math:`t_{TE}/c_{ax}`.
        Default is 0.04.
    tmax_stat2cax : float, optional
        Maximum stator blade thickness divided by axial chord: :math:`t_{s,max}/c_{ax}`.
        Default is 0.30.
    tmax_rot2cax : float, optional
        Maximum rotor blade thickness divided by axial chord: :math:`t_{r,max}/c_{ax}`.
        Default is 0.25.
    pos_tmax_stat2cax : float, optional
        Axial position of the stator section with maximum thickness, given as
        a fraction of the axial chord: :math:`z_{s,max,t}/c_{ax}`.
        Default is 0.45.
    pos_tmax_rot2cax : float, optional
        Axial position of the rotor section with maximum thickness, given as
        a fraction of the axial chord: :math:`z_{r,max,t}/c_{ax}`.
        Default is 0.40.
    pos_modLE2cax : float, optional
        **"fraction of axial chord over which the leading edge is modified"** ??
        Default is 0.02.
    pos_modTE2cax : float, optional
        **"fraction of axial chord over which the trailing edge is modified"** ??
        Default is 0.01.
    Zw : float, optional
        Zweifel's coefficient. Default is 0.85.
    exp : float, optional
        **"Exponent for transforming the axial position. It is used to vary the 
        camber line shape. increasing expo moves the blade loading upstream."** ??
        Default is 1.
    thetaLE2ax_merid_1 : float, optional
        Angle between the leading edge of the 1st row and the axial direction 
        in the meridional view [deg].
        Default is 92.0.
    thetaLE2ax_merid_2 : float, optional
        Angle between the leading edge of the 2nd row and the axial direction 
        in the meridional view [deg].
        Default is 88.0.
    thetaTE2ax_merid_1 : float, optional
        Angle between the trailing edge of the 1st row and the axial direction 
        in the meridional view [deg].
        Default is 88.0.
    thetaTE2ax_merid_2 : float, optional
        Angle between the trailing edge of the 2nd row and the axial direction 
        in the meridional view [deg].
        Default is 92.0.
    thickness_distribution : int, optional
        **"Form of blade thickness distribution"** ??
        Default is 2.
    """
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
    thickness_distribution: int = 2

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
class CompressorOpts(StageOpts):
    """
    Default parameters and options for a compressor stage.
    
    Parameters
    ----------
    tLE2cax : float, optional
        Leading-edge thickness divided by axial chord: :math:`t_{LE}/c_{ax}`.
        Default is 0.02.
    tTE2cax : float, optional
        Trailing-edge thickness divided by axial chord: :math:`t_{TE}/c_{ax}`.
        Default is 0.01.
    tmax_stat2cax : float, optional
        Maximum stator blade thickness divided by axial chord: :math:`t_{s,max}/c_{ax}`.
        Default is 0.10.
    tmax_rot2cax : float, optional
        Maximum rotor blade thickness divided by axial chord: :math:`t_{r,max}/c_{ax}`.
        Default is 0.075.
    pos_tmax_stat2cax : float, optional
        Axial position of the stator section with maximum thickness, given as
        a fraction of the axial chord: :math:`z_{s,max,t}/c_{ax}`.
        Default is 0.45.
    pos_tmax_rot2cax : float, optional
        Axial position of the rotor section with maximum thickness, given as
        a fraction of the axial chord: :math:`z_{r,max,t}/c_{ax}`.
        Default is 0.40.
    pos_modLE2cax : float, optional
        **"fraction of axial chord over which the leading edge is modified"** ??
        Default is 0.02.
    pos_modTE2cax : float, optional
        **"fraction of axial chord over which the trailing edge is modified"** ??
        Default is 0.01.
    Zw : float, optional
        Zweifel's coefficient. Default is 0.50.
    diffusion_factor : float, optional
        Diffusion factor for compressors, **NOT USED NOW??**.
        Default is 0.35.
    exp : float, optional
        **"Exponent for transforming the axial position. It is used to vary the 
        camber line shape. increasing expo moves the blade loading upstream."** ??
        Default is 1.
    thetaLE2ax_merid_1 : float, optional
        Angle between the leading edge of the 1st row and the axial direction 
        in the meridional view [deg].
        Default is 88.0.
    thetaLE2ax_merid_2 : float, optional
        Angle between the leading edge of the 2nd row and the axial direction 
        in the meridional view [deg].
        Default is 92.0.
    thetaTE2ax_merid_1 : float, optional
        Angle between the trailing edge of the 1st row and the axial direction 
        in the meridional view [deg].
        Default is 92.0.
    thetaTE2ax_merid_2 : float, optional
        Angle between the trailing edge of the 2nd row and the axial direction 
        in the meridional view [deg].
        Default is 88.0.
    thickness_distribution : int, optional
        **"Form of blade thickness distribution"** ??
        Default is 2.
    """
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


@dataclass
class GasModelOpts:
    """
    Options for the gas thermodynamic model.
    
    
    Parameters
    ----------
    gas_model : GasModel, optional
        Gas model.
    R : float, optional
        Massic gas constant [J/(kgK)]. Default is 287.15 J/kgK.
    gamma : float, optional
        Specific heat ratio :math:`c_p/c_v`. Default is 1.40.
    """
    gas_model: GasModel = GasModel.PERFECT
    # gas constant [J/kgK] (default: air)
    R: float = 287.15
    # gas specific heat ratio Cp/Cv (default: air)
    gamma: float = 1.40


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


