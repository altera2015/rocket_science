import math
import numpy as np
from vect import Vector

class Stage:

    """
    Stage constructor. A rocket is built out of 1 or more stages.

    dry_mass of stage without propellant in kg
    propellant_mass = mass of propellant in kg
    burn_time = burn time at 100% throttle till propellant is used up.    
    static_thrust = thrust at sea level in N
    diameter = diameter of stage in meters.
    jettison_after_use = boolean indicating if this stage is jettisoned when empty.
    """
    def __init__(self, dry_mass, propellant_mass, burn_time, static_thrust, diameter, jettison_after_use = True, name = ""):
        
        self.__dry_mass = dry_mass 
        self.__propellant_mass = propellant_mass
        self.__propellant_mass_at_start = propellant_mass
        if burn_time == 0:
            self.__propellant_100_percent_burn_rate = 0
        else:
            self.__propellant_100_percent_burn_rate = propellant_mass / burn_time
        
        self.__static_thrust = static_thrust
        self.__diameter = diameter
        self.__name = name
        self.__jettison_after_use = jettison_after_use
        self.__jettisoned = False
                        
        self.__throttle = 0.0
        self.__drag_surface = math.pi * ( self.__diameter / 2.0 ) ** 2
        self.__lastx = ""
        # advanced rocket engine equations
        self._ispVac = None
        self._exit_area = None
        #self.__ispVac = IspVac
        # self.exit_area = math.pi * ( 1.4 / 2.0 )**2

    @property
    def name(self):
        return self.__name

    @property
    def propellant_mass(self):
        return self.__propellant_mass

    @property
    def dry_mass(self):
        return self.__dry_mass

    @property
    def throttle(self):
        return self.__throttle
    
    @throttle.setter
    def throttle(self, value):
        self.__throttle = value

    @property
    def mass(self):
        return self.propellant_mass + self.dry_mass

    @property
    def drag_surface(self):
        return self.__drag_surface

    @property
    def jettison_after_use(self):
        return self.__jettison_after_use

    @property
    def jettisoned(self):
        return self.__jettisoned

    @jettisoned.setter
    def jettisoned(self, value):
        self.__jettisoned = value

    def burn(self, dt):
        self.__propellant_mass -= self.mass_flow() * dt
        if self.__propellant_mass < 0.0:
            self.__propellant_mass = 0.0            
        return self.__propellant_mass
    
    def mass_flow(self):

        if self.propellant_mass <= 0.0:
            return 0.0
        
        return self.throttle * self.__propellant_100_percent_burn_rate

    def thrust(self, p_external):
        
        if self.propellant_mass <= 0.0:
            return 0.0

        # https://en.wikipedia.org/wiki/Rocket_engine_nozzle
        if self._ispVac is not None:
            F = self._ispVac * 9.81 * self.mass_flow() - self._exit_area * p_external
            return F

        # x = "{}, thrust {},  throttle {}, st {}".format(self.__name, self.__static_thrust, self.throttle, self.throttle * self.__static_thrust)        
        # if x != self.__lastx:
        #     self.__lastx = x
        #     print(x)
        
        # Really only valid at sea level, needs improvement from rocket equation.        
        return self.__static_thrust * self.throttle
    
    def control( self, throttle):
        self.__throttle = throttle        