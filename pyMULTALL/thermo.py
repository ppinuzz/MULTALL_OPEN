#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thermodynamic utilities.

@author: Andrea Pinardi <andrea.pinardi@polimi.it>
"""

from abc import ABC, abstractmethod
from CoolProp import AbstractState
import CoolProp.CoolProp as CP
from defaults import THERMO_BACKEND
import numpy as np

# universal gas constant [J/k*mol]
R = 8.31446261815324

# -----------------------------------------------------------------------------
#                   SPECIFIC HEAT AT CONSTANT PRESSURE
# -----------------------------------------------------------------------------

# basic blueprint for any Cp model: it must provide a 
#   1) _Cp method that takes 2 float in input and returns a float and does the
#   actual calculation
#   2) a Cp method that checks the input and then calls _Cp to calculate the Cp
# ABC is a dummy class: it crashes if you try to instantiate CpModel directly
# in your code (being just "a blueprint", you cannot use it in your main code, 
# it's to be used by the Cp model methods only)
class CpModel(ABC):
    
    def Cp(self, T: float, p: float | None = None) -> float:
        if T <= 0:
            raise ValueError('Temperature must be > 0 K')
        if p is not None and p <= 0:
            raise ValueError('Pressure must be > 0 Pa')
        return self._Cp(T, p)
    
    @abstractmethod
    def _Cp(self, T: float, p: float | None = None) -> float:
        """Model specific Cp implementation [J/(kgK)]"""


# ---------------------------- ACTUAL Cp MODELS ----------------------------
class ConstantCp(CpModel):
    def __init__(self, Cp0: float):
        if Cp0 <= 0:
            raise ValueError('Constant Cp must be positive')
        self.Cp0 = Cp0

    def _Cp(self, T: float, p: float | None = None) -> float:
        return self.Cp0


class NASAPolynomialCp(CpModel):

    def __init__(self, coeffs: list[float], MM: float, Tmin: float | None, Tmax: float | None):
        if MM <= 0:
            raise ValueError('Molar mass must be > 0 g/mol')
        # use the _ to mark them as private
        # [J/(k*mol)] * [g/mol] = 1000 * [J/(k*mol)] * [kg/mol]
        self._R_mass = 1000 * R / MM
        # TODO: add support for piecewise Cp(T) definition
        self._NASApoly = lambda T: (coeffs[0]/T**2 + coeffs[1]/T + coeffs[2] + 
                                    coeffs[3]*T + coeffs[4]*T**2 + coeffs[5]*T**3 +
                                    coeffs[6]*T**4)
        self.Tmin = Tmin
        self.Tmax = Tmax

    def _Cp(self, T: float, p: float | None = None) -> float:
        invalid_temp_message = f'T = {T} K outside NASA validity range [{self.Tmin}, {self.Tmax}]'
        # short-circuiting: se la prima condizione è falsa, la seconda viene
        # ignorata (e non darà errore, come invece T < None darebbe)
        if (self.Tmin is not None and T < self.Tmin) or (self.Tmax is not None and T > self.Tmax):
            raise ValueError(invalid_temp_message)

        # NASA polynomials are written as Cp/R = f(T)
        Cp_dim = self._R_mass * self._NASApoly(T)
        
        return Cp_dim


class RealGasCp(CpModel):
    def __init__(self, fluid: str):
        self.FLUID = AbstractState(THERMO_BACKEND, fluid)

    # now p is actually required, but _Cp() interface as defined in the 
    # abstract method has p: float | None = None
    # keep the same signature, but add an error internally
    def _Cp(self, T: float, p: float | None = None) -> float:
        if p is None:
            raise ValueError(f'Real-gas Cp model requires pressure as input!')
        self.FLUID.update(CP.PT_INPUTS, p, T)
        Cp = self.FLUID.cpmass()
        return Cp


# -----------------------------------------------------------------------------
#                                   DENSITY
# -----------------------------------------------------------------------------

class DensityModel(ABC):
    
    def rho(self, T: float, p: float) -> float:
        if T <= 0:
            raise ValueError('Temperature must be > 0 K')
        if p <= 0:
            raise ValueError('Pressure must be > 0 Pa')
        return self._rho(T, p)
    
    @abstractmethod
    def _rho(self, T: float, p: float) -> float:
        """Model specific density implementation [kg/m3]"""


class IdealGasDensity(DensityModel):
    def __init__(self, MM: float):
        if MM <= 0:
            raise ValueError('Molar mass must be > 0 g/mol')
        # use the _ to mark them as private
        # [J/(k*mol)] * [g/mol] = 1000 * [J/(k*mol)] * [kg/mol]
        self._R_mass = 1000 * R / MM

    def _rho(self, T: float, p: float) -> float:
        rho = p / (self._R_mass * T)
        return rho

# since the ideal gas law holds for both perfect and ideal gases, just create
# a subclass => no "actual" use, but it's neater in the code to call a
# PerfectGasDensity, rather than an IdealGasDensity, object when using a perfect
# gas
class PerfectGasDensity(IdealGasDensity):
    pass

class RealGasDensity(DensityModel):
    def __init__(self, fluid: str):
        self.FLUID = AbstractState(THERMO_BACKEND, fluid)

    def _rho(self, T: float, p: float) -> float:
        self.FLUID.update(CP.PT_INPUTS, p, T)
        rho = self.FLUID.rhomass()
        return rho


# -----------------------------------------------------------------------------
#                                   ENTHALPY
# -----------------------------------------------------------------------------

class EnthalpyModel(ABC):
    
    def h(self, T: float, p: float | None = None) -> float:
        if T <= 0:
            raise ValueError('Temperature must be > 0 K')
        if p is not None and p <= 0:
            raise ValueError('Pressure must be > 0 Pa')
        return self._h(T, p)
    
    @abstractmethod
    def _h(self, T: float, p: float | None = None) -> float:
        """Model specific enthalpy implementation [J/kg]"""


class PerfectGasEnthalpy(EnthalpyModel):
    def __init__(self, Cp_perfect: ConstantCp):
        self.Cp_perfect = Cp_perfect

    def _h(self, T: float, p: float | None) -> float:
        Cp = self.Cp_perfect.Cp(T)
        h = Cp * T
        return h


class NASAPolynomialEnthalpy(EnthalpyModel):

    def __init__(self, coeffs: list[float], MM: float, Tmin: float | None, Tmax: float | None):
        if MM <= 0:
            raise ValueError('Molar mass must be > 0 g/mol')
        # use the _ to mark them as private
        # [J/(k*mol)] * [g/mol] = 1000 * [J/(k*mol)] * [kg/mol]
        self._R_mass = 1000 * R / MM
        # TODO: add support for piecewise h(T) definition
        self._NASApoly = lambda T: (-coeffs[0]/T**2 + coeffs[1]*np.log(T)/T + 
                                    coeffs[2] + coeffs[3]*T/2 + coeffs[4]*T**2/3 +
                                    coeffs[5]*T**3/4 + coeffs[6]*T**4/5 + 
                                    coeffs[7]/T)
        self.Tmin = Tmin
        self.Tmax = Tmax

    def _h(self, T: float, p: float | None = None) -> float:
        invalid_temp_message = f'T = {T} K outside NASA validity range [{self.Tmin}, {self.Tmax}]'
        # short-circuiting: se la prima condizione è falsa, la seconda viene
        # ignorata (e non darà errore, come invece T < None darebbe)
        if (self.Tmin is not None and T < self.Tmin) or (self.Tmax is not None and T > self.Tmax):
            raise ValueError(invalid_temp_message)

        # NASA polynomials are written as h/RT = f(T)
        h_dim = self._R_mass * T * self._NASApoly(T)
        
        return h_dim


class RealGasEnthalpy(EnthalpyModel):
    def __init__(self, fluid: str):
        self.FLUID = AbstractState(THERMO_BACKEND, fluid)

    def _h(self, T: float, p: float | None) -> float:
        if p is None:
            raise ValueError(f'Real-gas enthalpy model requires pressure as input!')
        self.FLUID.update(CP.PT_INPUTS, p, T)
        h = self.FLUID.hmass()
        return h

if __name__ == '__main__':
    T = 300
    p = 1e5
    fluid = 'H2'
    
    Cp_H2 = 14.31e3
    MyCp_cost = ConstantCp(Cp0=Cp_H2)
    Cp_calc = MyCp_cost.Cp(T, p)
    print(f'{Cp_calc}')
    
    # 7 Cp(T)/R constants + last h(T)/RT constant + last s(T)/R constant
    coeffs = [4.078323210e+04, -8.009186040e+02, 8.214702010e+00, 
              -1.269714457e-02, 1.753605076e-05, -1.202860270e-08,
              3.368093490e-12, 2.682484665e+03, -3.043788844e+01]
    MyCp = NASAPolynomialCp(coeffs=coeffs, MM=2.016, Tmin=200, Tmax=1000)
    Cp_calc = MyCp.Cp(T, p)
    print(f'{Cp_calc}')
    
    MyCp = RealGasCp(fluid='H2')
    Cp_calc = MyCp.Cp(T, p)
    print(f'{Cp_calc}')
    
    MyRho = PerfectGasDensity(MM=2.016)
    rho_calc = MyRho.rho(T, p)
    print(f'{rho_calc}')
    
    MyRho = IdealGasDensity(MM=2.016)
    rho_calc = MyRho.rho(T, p)
    print(f'{rho_calc}')
    
    MyRho = RealGasDensity(fluid='H2')
    rho_calc = MyRho.rho(T, p)
    print(f'{rho_calc}')
    
    MyH = PerfectGasEnthalpy(Cp_perfect=MyCp_cost)
    h_calc = MyH.h(T, p)
    print(f'{h_calc}')
    
    MyH = NASAPolynomialEnthalpy(coeffs=coeffs, MM=2.016, Tmin=200, Tmax=1000)
    h_calc = MyH.h(T, p)
    print(f'{h_calc}')
    
    MyH = RealGasEnthalpy(fluid='H2')
    h_calc = MyH.h(T, p)
    print(f'{h_calc}')