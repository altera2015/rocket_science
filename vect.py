import math
import numpy as np
import unittest

"""
Vector class. Handles all your 3d calculations
"""
class Vector:

    """
    constructor creates a deep copy of the other parameter
    """
    def __init__(self, other = None):
        
        self._magnitude = None
        if other is None:
            self._pos = [0.0, 0.0, 0.0]
        else:
            self._pos = [
                other[0], other[1], other[2]
            ]

    def __getitem__(self, key):
        return self._pos[key]

    def __setitem__(self, key, value):
        self._magnitude = None
        self._pos[key]=value

    def __str__(self):
        return "({},{},{})".format(self._pos[0], self._pos[1], self._pos[2])

    """
    Zero out all elements.
    """
    def zero(self):
        self._magnitude = 0.0
        self._pos[0] = 0.0
        self._pos[1] = 0.0
        self._pos[2] = 0.0

    """
    Calculates the Euclidean norm
    """
    @property
    def magnitude(self):
        if self._magnitude == None:
            self._magnitude = np.linalg.norm(self._pos)
        return self._magnitude

    """
    Calculate Theta in ISO system
    (Inclination)
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#/media/File:3D_Spherical.svg
    """
    @property
    def theta(self):
        return math.acos( self._pos[2] / self.magnitude )

    """
    Calculate Theta in ISO system
    (Azimuth)
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#/media/File:3D_Spherical.svg
    """
    @property
    def phi(self):
        return math.atan2( self._pos[1], self._pos[0] )

    """
    Converts the Carthesian coordinates to spherical system
    """
    @staticmethod
    def toSpherical( vect ):
        r = np.linalg.norm(vect._pos)
        theta = math.acos( vect[2] / r)
        phi = math.atan2( vect[1], vect[0] )
        return [r,theta, phi]

    """
    Converts the coordinates from spherical to Carthesian
    """
    @staticmethod
    def toCartesian( vect ):
        x = vect[0] * math.sin( vect[1] ) * math.cos( vect[2] )
        y = vect[0] * math.sin( vect[1] ) * math.sin( vect[2] )
        z = vect[0] * math.cos( vect[2] )
        return [x,y,z]

    """
    Copy of the parametes
    """
    def assign( self, other ):
        self._magnitude = None
        self[0] = other[0]
        self[1] = other[1]
        self[2] = other[2]
        return self
    
    """
    Multiply the vector with a float
    """
    def mult( self, factor ):
        self._magnitude = None
        self[0] *= factor
        self[1] *= factor
        self[2] *= factor
        return self

    """
    Add another vector to self
    """
    def add( self, other ):
        self._magnitude = None
        self[0] += other[0]
        self[1] += other[1]
        self[2] += other[2]
        return self

    """
    Subtract another vector from self
    """
    def sub( self, other):
        self._magnitude = None
        self[0] -= other[0]
        self[1] -= other[1]
        self[2] -= other[2]
        return self

    """
    Create a deepcopy of the vector
    """
    def deepcopy(self):
        return Vector(self)

    def normalize(self):
        self.mult( 1.0 / self.magnitude )

    def __mul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __rmul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __add__(self, other):
        n = Vector(self)
        return n.add(other)

    def __radd__(self, other):
        n = Vector(other)
        return n.add(self)

    def __sub__(self, other):
        n = Vector(self)
        return n.sub(other)

    def __rsub__(self, other):
        n = Vector(other)
        return n.sub(self)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return np.all( np.isclose(self._pos, other._pos) )
        else:
            return np.all(np.isclose(self._pos, other))

        

class VectorUnitTest(unittest.TestCase):

    def test_equals(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([11.0, 12.0, 13.0])
        b.mult(0.1)
        self.assertTrue( a == b )

    def test_assign(self):
        a = Vector([1.0, 2.0, 3.0])        
        b = Vector()
        b.assign(a)
        self.assertTrue( a == b )
        c = b
        d = b.deepcopy()
        b.mult(2.0)
        self.assertFalse( a == b )
        self.assertFalse( a == c )
        self.assertTrue( a == d )

    def test_add(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([2.0, 3.0, 4.0])
        c = Vector([3.1, 4.2, 5.3])
        d = a + b
        self.assertTrue( d == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        self.assertTrue( b == Vector([2.0, 3.0, 4.0]) )

    def test_sub(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([2.0, 3.0, 4.0])
        c = Vector([-0.9, -1.8, -2.7])
        d = a - b
        self.assertTrue( d == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        self.assertTrue( b == Vector([2.0, 3.0, 4.0]) )


    def test_mult(self):
        a = Vector([1.1, 1.2, 1.3])        
        b = Vector([2.2, 2.4, 2.6])
        c = a * 2.0
        self.assertTrue( b == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        c = 2.0 * a
        self.assertTrue( b == c )

    def test_magnitude(self):
        a = Vector([1.0, 2.0, 3.0])        
        self.assertTrue( a.magnitude == math.sqrt(14.0) )
        a = a * 2.0
        self.assertTrue( a.magnitude == math.sqrt(56.0) )


if __name__ == '__main__':
    unittest.main()