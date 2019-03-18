# File encapsulating large bodies like planets
import numpy as np
import constants
import math
import jacchia


# Base class for Bodies in space. Like planets, or moons.
class Body:

    # Constructor
    # Radius = radius of body in meters
    # Mass = Mass of body in Kg
    # Name = human readable description of body.
    def __init__(self, radius, mass, name=""):
        self.__name = name
        self.__radius = radius
        self.__mass = mass

    @property
    def name(self):
        return self.__name

    @property
    def mass(self):
        return self.__mass

    @property
    def radius(self):
        return self.__radius

    # Must be overriden in child class.
    # returns [air pressure in Pascal, air density in kg/m3]
    # altitude is height above surface of body in meters.
    def air_pressure_and_density(self, altitude):
        print("Body::air_pressure not defined.")
        exit(-1)


    # https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
    # returns gravity in m/s^2
    def accelleration(self, altitude):
        radius = self.__radius + altitude        
        return [0,0, -( self.__mass * constants.G) / (radius*radius)]

class Earth(Body):
    
    def __init__(self):
        super().__init__(constants.earth_radius, constants.earth_mass, "Earth")

    def air_pressure_and_density(self, altitude):
        return jacchia.air_pressure_and_density(altitude)
