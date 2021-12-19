## @ingroup Attributes-Solids

# MLI.py
#
# Created: Dec, 2021, J. Kho

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from .Solid import Solid
from SUAVE.Core import Units

#-------------------------------------------------------------------------------
# Multi-Layer Insulation Solid Class
#-------------------------------------------------------------------------------

## @ingroup Attributes-Solid
class MLI(Solid):

    """ Physical Constants Specific to **Need to determine specific MLI**
    
    Assumptions:
    None
    
    Source:
    
    
    Inputs:
    N/A
    
    Outputs:
    N/A
    
    Properties Used:
    None
    """

    def __defaults__(self):
        """Sets material properties at instantiation.
        
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        N/A

        Outputs:
        N/A

        Properties Used:
        None
        """
        self.density                    = 50. * Units['kg/(m**3)']
        self.thermal_conductivity       = 1.e-4 * Units['W/m K']