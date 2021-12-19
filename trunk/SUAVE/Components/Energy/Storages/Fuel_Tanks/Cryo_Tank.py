## @ingroup Components-Energy-Storages-Fuel_Tanks
# Fuel_Tank.py
# 
# Created:  

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
from numpy import pi, sqrt, log, exp
import SUAVE

# package imports

from SUAVE.Core import Data
from SUAVE.Components.Energy.Energy_Component import Energy_Component

# ----------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------    

## @ingroup Components-Energy-Storages-Fuel_Tank
class Cryo_Fuel_Tank(Energy_Component):
    """
    Energy Component object that stores cryogenic fuel. Contains values
    used to indicate its fuel type.
    """
    def __defaults__(self):
        #self.mass_properties.empty_mass            = 0.0
        #self.mass_properties.fuel_mass_when_full   = 0.0
        #self.mass_properties.fuel_volume_when_full = 0.0
        self.diameter_internal                     = 0.0    #[m]
        self.length_internal                       = 0.0    #[m]
        self.design_pressure                       = 0.0    #[Pa]
        self.design_boiloff_rate                   = 0.0    #[kg/s]
        self.temperature_outer                     = 0.0    #[K]
        self.safety_factor_wall                    = 2.25    
        self.safety_factor_insulation              = 1.2
        self.fuel_type                             = None   # Propellant Class
        self.structural_material                   = None   # Solid Material Class
        self.insulation_material                   = None   # Solid Material Class

    def calculate_all(self):
        self.tank_type()
        self.calculate_structural_thickness()
        self.calculate_insulation_thickness()
        self.calculate_structural_mass()
        self.calculate_insulation_mass()
        self.calculate_fuel()

        self.mass_properties.empty_mass = self.mass_properties.structural + self.mass_properties.insulation
        print("calculated all properties")
        return


    def tank_type(self):
        if (self.diameter_internal == self.length_internal):
            self.tank_type = 'spherical'
        else:
            self.tank_type = 'cylindrical'
        return
        
    def calculate_structural_thickness(self):

        #calculate minimum structural wall thickness
        if (self.tank_type == 'spherical'):
            #spherical tank
            t_min = 0.5*self.diameter_internal*( ( 1 - 1.5 * self.design_pressure / self.structural_material.yield_tensile_strength)**(-1/3) - 1)
        else:
            #cylindrical tank
            t_min = 0.5 * self.diameter_internal * ( ( 1 - sqrt(3) * self.design_pressure / self.structural_material.yield_tensile_strength)**(-0.5) - 1)
        #calculate actual structural wall thickness using safety factor
        self.thickness_structural = self.safety_factor_wall * t_min
        return

    def calculate_structural_mass(self):
        #calculate mass of stuctural tank
        if (self.tank_type == 'spherical'):
            #spherical tank
            self.mass_properties.structural = self.structural_material.density * ( 4/3 * pi) * ( (0.5 * self.diameter_internal + self.thickness_structural)**3 - (0.5 * self.diameter_internal)**3)       #volume of thin-walled spherical shell 
        else:
            self.mass_properties.structural = self.structural_material.density * ( ( 4/3 * pi) * ( (0.5 * self.diameter_internal + self.thickness_structural)**3 - (0.5 * self.diameter_internal)**3) \
                + pi * ((0.5 * self.diameter_internal + self.thickness_structural)**2 - (0.5 * self.diameter_internal)**2) * (self.length_internal - self.diameter_internal))        #volume of thin-walled spherical shell with thin walled cylinder in the middle
        return

    def calculate_insulation_thickness(self):
        Q = self.design_boiloff_rate * self.fuel_type.enthalpy_vaporisation
        if (self.tank_type == 'spherical'):
            alpha = (4 * pi/Q) * (self.temperature_outer - self.fuel_type.temperatures.storage)
            beta = (1 / self.structural_material.thermal_conductivity) * ( 1/(0.5 * self.diameter_internal) - 1/(0.5*self.diameter_internal + self.thickness_structural))
            gamma = alpha - beta

            t_min = (0.5 *  self.diameter_internal + self.thickness_structural) *  (gamma * self.insulation_material.thermal_conductivity)/(1 - gamma*self.insulation_material.thermal_conductivity)
        
        else:
            alpha = (2 * pi * self.length_internal/Q) * (self.temperature_outer - self.fuel_type.temperatures.storage)
            beta = (1 / self.structural_material.thermal_conductivity) * log((0.5*self.diameter_internal + self.thickness_structural)/ (0.5 * self.diameter_internal))
            gamma = alpha - beta

            t_min = (0.5 *  self.diameter_internal + self.thickness_structural) *  ( exp(gamma * self.insulation_material.thermal_conductivity) -1)

        self.thickness_insulation = self.safety_factor_insulation * t_min
        return

    def calculate_insulation_mass(self):
        if (self.tank_type == 'spherical'):
            self.mass_properties.insulation = self.insulation_material.density * (4/3*pi) * ((0.5 * self.diameter_internal + self.thickness_structural + self.thickness_insulation)**3 - (0.5*self.diameter_internal + self.thickness_structural)**3)
        else:
            self.mass_properties.insulation = self.insulation_material.density * ( (4/3*pi) * ((0.5 * self.diameter_internal + self.thickness_structural + self.thickness_insulation)**3 - (0.5*self.diameter_internal + self.thickness_structural)**3) \
                + pi* ((0.5 * self.diameter_internal + self.thickness_structural + self.thickness_insulation)**2 - (0.5* self.diameter_internal + self.thickness_structural)**2) * (self.length_internal - self.diameter_internal)) 
        return

    def calculate_fuel(self):
        if (self.tank_type == 'spherical'):
            self.mass_properties.fuel_volume_when_full = 1/6 * pi * self.diameter_internal**3
        else:
            self.mass_properties.fuel_volume_when_full = (1/6 * pi * self.diameter_internal**3) + (0.25 * pi * self.diameter_internal**2 * (self.length_internal - self.diameter_internal)) 

        self.mass_properties.fuel_mass_when_full = self.mass_properties.fuel_volume_when_full * self.fuel_type.density
        return





        


