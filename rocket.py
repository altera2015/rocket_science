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
from vect import Vector

class Rocket:

    """
    Rocket Constructor
    takes a list of stages
    
    Rocket currently is simulated as a point mass. Real geometry will be later.

    Only simple stacked stages for now. Side boosters in next iteration.

    max_force = maximum force the airframe can handle.
    position = cartesian coordinates ( body center is 0,0 )
    velocity = orientation, please face rocket pointing up!
    """
    def __init__(self, stages, max_force, position, orientation = None):

        self.__stages = stages
        self.__current_stage = 0
        self.__max_force = max_force
        self.__position = position
        

        if orientation == None:
            # pick orientation orthogonal to surface.
            self.__orientation = self.__position.deepcopy().normalize()            
        else:
            self.__orientation = orientation

        self.__velocity = Vector()
        self.__drag = Vector()
        self.__thrust = Vector()
        self.__throttle = 0.0
        

    @property
    def max_forces(self):
        return self.__max_force

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value
    

    def drag_coefficient(self):
        # really this is dependent on velocity and vehicle configuration 
        # see https://space.stackexchange.com/questions/12649
        return 0.30


    def drag(self, atmosphere_mass_density):

        # find the wides part of the rocket and
        # use that for drag calculations
        max_drag_surface = 0.0
        for stage in self.__stages:
            if not stage.jettisoned and stage.drag_surface >= max_drag_surface:
                max_drag_surface = stage.drag_surface

        # Get velocity
        velocity = self.__velocity.magnitude

        # No speed, no drag!
        if ( velocity == 0.0 ):
            self.__drag.zero()
            return self.__drag
        
        # Calculate drag depends on atmosphere of course
        f = -0.5 * atmosphere_mass_density * velocity * velocity * self.drag_coefficient() * max_drag_surface
        
        # Force is directed against the velocity vector.
        return self.__drag.assign(self.velocity).mult(f / velocity)
        

    def mass(self):

        mass = 0.0
        for stage in self.__stages:
            if not stage.jettisoned:
                mass += stage.mass

        return mass


    def thrust(self, p_external):

        # Only the lowest stage can be active at any time for now.
        # Once we get multiple stages running at the same time 
        # this will change a bit.
        stage = self.__stages[self.__current_stage] 
        
        if stage.propellant_mass <= 0.0:
            self.__thrust.zero()
            return self.__thrust

        
        F = stage.thrust(p_external)        
        return self.__thrust.assign(self.__orientation).mult(F)        

    def time_step(self, dt, t):
        
        stage = self.__stages[self.__current_stage]
        
        propellant_left = stage.burn(dt)
        if propellant_left <= 0.0 and stage.jettison_after_use and self.__current_stage < len(self.__stages) - 1:
            print("Staging! {} jettisoning {}, next stage = {}".format(t, self.__stages[self.__current_stage].name, self.__stages[self.__current_stage+1].name))
            self.__current_stage = self.__current_stage + 1
            stage.jettisoned = True
            self.__stages[self.__current_stage].throttle = self.__throttle
            print("Force from stage {} = {}".format(self.__stages[self.__current_stage].name, self.__stages[self.__current_stage].thrust(0.0)))
            

    @property
    def throttle(self):
        return self.__throttle

    @throttle.setter
    def throttle(self, value):
        self.__throttle = value
        stage = self.__stages[self.__current_stage]
        stage.throttle = value

    # Once we go away from point source we can calculate 
    # orientation based on forces. For now fake it!
    def set_orientation(self, orientation):
        self.__orientation = orientation