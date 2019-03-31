# File encapsulating large bodies like planets
import numpy as np
import constants
import math
import jacchia
from vect import Vector
import unittest


# Base class for Bodies in space. Like planets, or moons.
class Body:

    # Constructor
    # Radius = radius of body in meters
    # Mass = Mass of body in Kg
    # Name = human readable description of body.
    def __init__(self, radius, mass, rotation_period, name=""):
        self.__name = name
        self.__radius = radius
        self.__mass = mass
        self.__rotation_period = rotation_period * 1.0

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
    def accelleration(self, position):
        
        radius = position.magnitude
        v = Vector( position )
        a = -( self.__mass * constants.G) / (radius*radius)
        v.mult( a / position.magnitude )
        
        return v

    def surface_speed( self, position ):
        # just returning equator right now.
        # todo fix for inclination.
        speed = math.pi * 2 * self.__radius / self.__rotation_period
        return Vector( [ -position[1], position[0], 0.0 ] ).normalize().mult(speed)         

class Earth(Body):
    
    def __init__(self):
        super().__init__(constants.earth_radius, constants.earth_mass, 24 * 60 * 60, "Earth")

    def air_pressure_and_density(self, position):
        altitude = position.magnitude - self.radius
        return jacchia.air_pressure_and_density(altitude)



class EarthUnitTest(unittest.TestCase):
    
    def test_pressure(self):
        
        earth = Earth()  
        pos = Vector([0.0, earth.radius, 0.0])
        p, d = earth.air_pressure_and_density(pos)
        print(p,d)
        self.assertTrue( p >= 101e3 and p < 102e3 )

    def test_velocity(self):
        
        earth = Earth()  
        pos = Vector([0.0, earth.radius, 0.0])
        velocity = earth.surface_speed(pos)
        #print(velocity)
        v = velocity.magnitude
        self.assertTrue( v >=  460 and v <= 465 )


if __name__ == '__main__':
    unittest.main()