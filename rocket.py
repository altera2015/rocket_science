# Rocket class
# Encapsulate the rocket characteristics & dynamics
#
# https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation
# https://en.wikipedia.org/wiki/Rocket_engine_nozzle
# https://en.wikipedia.org/wiki/Atlas_V#Atlas_V_first_stage
# https://en.wikipedia.org/wiki/Comparison_of_orbital_rocket_engines
import numpy as np
import constants
import math

class Rocket:
    
    def __init__(self):
        # Atlas 5 first stage
        # kg
        self.dry_mass = 21054 + 23000 + 20000 # 23 = 2nd stage, 20 = payload to LEO
        # kg
        self.propellant_mass = 284089
        self.burn_time = 253
        # thrust at SL in N
        self._thrust = 3827e3
        # specific impulse s
        self.IspVac = 337.8
        self.diameter = 3.81
        self.drag_surface = math.pi * ( self.diameter / 2.0 ) ** 2
        
        self.propellant_mass_left = self.propellant_mass
        self.position = [0.0, 0.0, 0.0]
        self.velocity = [0.0, 0.0, 0.0]
        #self.acceleration = [0.0, 0.0]
        
        self.exit_area = math.pi * ( 1.4 / 2.0 )**2
    
    def mass(self):
        return self.dry_mass + self.propellant_mass_left

    def burn(self, dt):
        self.propellant_mass_left -= self.mass_flow() * dt

    def mass_flow(self, throttle = 1.0):

        if self.out_of_propellant():
            return 0.0

        return throttle * self.propellant_mass / self.burn_time

    def out_of_propellant(self):
        return self.propellant_mass_left < 0

    def thrust(self, p_external):
        
        if self.out_of_propellant():
            return [0.0, 0.0, 0.0]

        # https://en.wikipedia.org/wiki/Rocket_engine_nozzle
        # F = self.IspVac * 9.81 * self.mass_flow() - self.exit_area * p_external
        
        # Really only valid at sea level, needs improvement from rocket equation.
        F = self._thrust
        return [0.0, 0.0, F]

    def drag_coefficient(self):
        # really this is dependent on velocity, see 
        # https://space.stackexchange.com/questions/12649
        return 0.30

    def drag(self, mass_density):
        
        velocity = np.linalg.norm( self.velocity )
        if ( velocity == 0.0 ):
            return [0.0,0.0,0.0]

        #print(velocity)
        f = -0.5 * mass_density * velocity * velocity * self.drag_coefficient() * self.drag_surface

        drag = [ 0,0,0 ]
        drag[0] = self.velocity[0] / velocity * f
        drag[1] = self.velocity[1] / velocity * f
        drag[2] = self.velocity[2] / velocity * f

        return drag
